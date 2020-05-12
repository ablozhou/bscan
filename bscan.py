#!/usr/bin/env python3
# encoding: utf-8
'''
BScan: a web page  scan tool for php, java, asp, aspx, directory.
Date: 2020-05-12
Author: zhouhh
Copyright (c) 2020—2025 zhouhh <ablozhou # gmail.com> All rights reserved.
'''

import requests
import threading
import time
import os
from getopt import gnu_getopt;
import sys
import threading
from concurrent.futures import ThreadPoolExecutor,as_completed

conf_path = './conf/'

class biscan:
    def __init__(self):
        self.lang=[]  # languages
        self.confs=[] # configure files
        self.threads=[]
        self.output='out.txt' # output file name
        self.timeout_seconds=3 
        self.threads_count=20
        self.host=None

    def getopts(self):
        opts, args = gnu_getopt(sys.argv[1:], "s:t:o:l:h:", ["help", "output="])#"ho:"=='-h-o:'
        print('options:{0}'.format(opts))
        print('args:{0}'.format(args))
        for o, a in opts:
            if o == "--help":
                print("help:")
                self.usage()
                sys.exit()
            if o in ("-o", "--output"):
                self.output = a
            if o =="-s":
                self.timeout_seconds=a
            if o =="-t":
                self.threads_count=a
            if o =="-l":
                self.lang.append(a)
            if o =="-h":
                self.host=a

        if self.host == None or len(opts)<1:
            print('host:{0}'.format(self.host))

            self.usage()
            sys.exit()


    def usage(self):
        u='''   python biscan.py [options] -h host[:port]
        host: the target host to scan
        port: the port of the web. default is 80.
        options:
            -s seconds: timeout seconds. default is 5 sec.
            -t threads: threads count. default is 20.
            -o ofile, --output=ofile: output log file
            -l lang: program language of the web server. default is all. 
                new language must set in the conf directory.
            --help: print this message.
        example:
            python biscan.py -l php -l java -h 192.168.2.3

        '''
        print(u)
         
    def read_conf(self,confpath):
        # pwd = os.getcwd()
        confs=[]

        confs =  os.listdir(confpath)
        
        for c in confs:
            
            fname,ext = os.path.splitext(os.path.basename(c))
            if len(self.lang) > 0 and fname not in self.lang:
                continue

            self.confs.append(os.path.join('%s%s' % (confpath, c)))
    
    def scan(self,host,file_path):
        url = host + file_path
        #print('scan {}'.format(url))
        headers1 = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://baidu.com'
        }
    
        data="?id=1"
        try:
            res = requests.get(url,headers=headers1,timeout=self.timeout_seconds)
            res = requests.post(url+data,headers=headers1,timeout=self.timeout_seconds)
        except Exception as e:
            if str(e).find('timed out') != -1:
                # retry
                # scan(host, payload)
                print("time out:",url)
                return 2,url
            
            print(e)
            return 3
        
        if res.status_code==200:
            print(url , res.status_code)
            return 0,url
        return 1,url

    def run(self):
        self.getopts()
        self.read_conf(conf_path)
        print('======  beginning scan ... =======')
            
        host = "http://" + self.host + "/"
        paths=""
        with ThreadPoolExecutor(max_workers=self.threads_count) as executor:
            tasks=[]
            for f in self.confs:
                print("config:"+f)
                with open(f,'r',encoding='utf8') as fin:
                    for line in fin.readlines():
                        try:
                            
                            paths = line.strip("\r").strip("\n").replace(' ', '')

                        except Exception as e:
                            print(e)
                            #paths = line.decode('gbk').strip("\r").strip("\n").replace(' ', '')
            
                        if paths == "":
                            #print("paths is empty")
                            continue
            
                        #print("line:"+paths)
                        
                        t=executor.submit(self.scan,host,paths)
                        tasks.append(t)

            for future in as_completed(tasks):
                code,data = future.result()
                if code == 0:
                    print("ok:{}".format(data))
        
        print("====== finished! =======")
 
if __name__ == '__main__':
    s = biscan()
    s.run()
 
    
 
 
 