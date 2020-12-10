# BScan
a python3 security tool which scan files and paths for a web backend.

类御剑扫描服务器网站url暴露文件的开源工具
可以用于发现某些网站是否存在admin.php, admin/, login.php, login/, admin_login, login.php.bak等 url，

扫描结果可以用于发现网站漏洞。

# install
```
pip install -r requirements.txt

```

# useage
```
   python bscan.py [options] -h host[:port]
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

```