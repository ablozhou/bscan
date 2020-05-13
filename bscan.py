#!/usr/bin/env python3
# encoding: utf-8
'''
BScan: a web page  scan tool for php, java, asp, aspx, directory.
Date: 2020-05-12
Author: zhouhh
Copyright (c) 2020—2025 zhouhh <ablozhou # gmail.com> All rights reserved.
'''

import grequests
import threading
import time
import os
from getopt import gnu_getopt;
import sys
import logging

config={
    'conf_path' : './conf/',
    'out_path' : './out/',
    'out_file' : 'out.txt',
    'headers': {
                'Accept': '*/*',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                'Cache-Control': 'no-cache',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': 'https://baidu.com'
            }
}

class FileHandler(logging.Handler):
    def __init__(self, file_path):
        self._fd = os.open(file_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND)
        logging.Handler.__init__(self)

    def emit(self, record):
        msg = "{}\n".format(self.format(record))
        os.write(self._fd, msg.encode('utf-8'))

class bscan:
    def __init__(self):
        self.lang=[]  # languages
        self.confs=[] # configure files
        self.threads=[]
        self.output=config['out_path']+config['out_file'] # output file name
        self.timeout_seconds=3 
        self.threads_count=20
        self.host=None
        self.fh = None # file handler for output
        sh = logging.StreamHandler() # stream handler like stdout
        self.logger = logging.getLogger('bscan')
        self.logger.addHandler(sh)
        self.logger.setLevel(logging.DEBUG)
        if not os.path.exists(config['out_path']):
            os.mkdir(config['out_path'])

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
                self.output = config['out_path']+a
                if self.fh != None:
                    self.logger.removeHandler(self.fh)
                self.fh = FileHandler(self.output)
                self.fh.setLevel(logging.INFO)
                self.logger.addHandler(self.fh)
            if o =="-s":
                self.timeout_seconds=a
            if o =="-t":
                self.threads_count=a
            if o =="-l":
                self.lang.append(a)
            if o =="-h":
                if not a.startswith("http://") or not a.startswith("https://"):
                    self.host="http://"+a
                if a[-1:]!='/':
                    self.host+='/'

        if self.fh == None:
            self.fh = FileHandler(self.output)
            self.fh.setLevel(logging.INFO)
            self.logger.addHandler(self.fh)

        if self.host == None or len(opts)<1:
            print('host:{0}'.format(self.host))

            self.usage()
            sys.exit()


    def usage(self):
        u='''   python bscan.py [options] -h host[:port]
        host: the target host to scan, default schema is http.
        port: the port of the web. default is 80.
        options:
            -s seconds: timeout seconds. default is 3 sec.
            -t threads count: threads count. default is 20.
            -o ofile, --output=ofile: output log file
            -l lang: program language of the web server. default is all. 
                new language must set in the conf directory.
            --help: print this message.
        example:
            python bscan.py -l php -l test -h http://192.168.2.3:8080

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
    
    def resp(self, r, *args, **kwargs):
        # print(r.url)
        if r.status_code == 200:
            self.logger.info(r.url)

    def run(self):
        self.getopts()
        self.read_conf(config['conf_path'])
        print('======  beginning scan ... =======')
        paths=""
        
        for f in self.confs:
            print("config:"+f)
            with open(f,'r',encoding='utf8') as fin:
                tasks=[]
                for line in fin.readlines():
                    try:
                        paths = line.strip("\r").strip("\n").replace(' ', '')
                    except Exception as e:
                        print(e)
        
                    if paths == "":
                        #print("paths is empty")
                        continue
        
                    url=self.host+paths
                    #print("url:{}".format(url))

                    req = grequests.get(url, callback=self.resp)
                    req = grequests.post(url, callback=self.resp)
                    tasks.append(req)
                res = grequests.map(tasks, size=self.threads_count,gtimeout=self.timeout_seconds)


            
        
        print("====== finished! =======")
 
if __name__ == '__main__':
    s = bscan()
    s.run()
 
    
 
 
 