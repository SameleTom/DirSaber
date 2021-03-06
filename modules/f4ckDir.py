#!/usr/bin/env python2
#-*-encoding:utf-8-*-
from modules.Saber_col import printError, printWait, printResult
from lib.logging import logging
import urllib2,sys,threading,Queue,time
from lib.proxy import proxycheck,myproxy
from lib.ThreadGetKey import ThreadGetKey
import os

def f4ckDir(site,sdir,smode,sproxy = None, sscript = None):
    if sproxy:
        connet_proxy = myproxy(sproxy)
        if not connet_proxy:
            printError("proxy Error!!")
            sys.exit(1)
    try:
        filename = site.replace ("http://","").replace ("/","")
        ldir = "/".join(sdir.split("/")[0:-2])
        logging_file=logging(ldir+"/log/"+filename+".txt")

    except Exception,e:
        print e
        pass

    global queue
    queue = Queue.Queue()
    threads = []

    if sdir.split('.')[-1] != "txt":
        files = os.listdir(sdir)
        for searchfile in files:
             if searchfile.split('.')[-1] == "txt":
                with open(sdir+searchfile) as dirfile:
                    for line in dirfile:
                        line = line.strip("\r").strip("\n")
                        if sscript and line.find(".") and line.split(".")[-1] == sscript:
                            queue.put(line) 
                        elif not sscript:
                            queue.put(line)
    else:
        with open(sdir) as dirfile:
            for line in dirfile:
                line = line.strip("\r").strip("\n")
                if sscript and line.find(".") and line.split(".")[-1] == sscript:
                    queue.put(line) 
                elif not sscript:
                    queue.put(line)
    ######################################################
    #shouhu_pro & jindu_pro
    shouhu = ThreadGetKey()
    shouhu.setDaemon(True)
    shouhu.start()

    # maxloading = queue.qsize()
    # view_loading = Loading(maxloading)
    # view_loading.start()

    #########################################################
    #lines start!
    for i in range(10):
        a = finder(site,smode,logging_file)
        a.start()
        threads.append(a)
    for j in threads:
        j.join()
            
    printWait(smode+"------->" + "task".ljust(48,' ') + "[ALL DONE]")
    try:
        logging_file.close()
    except:
        pass

class finder(threading.Thread):
    def __init__(self,site,smode,logging_file):
        threading.Thread.__init__(self)
        self.site = site
        self.smode = smode
        self.logging_file = logging_file

    def run(self):
        while 1:
            if queue.empty()== True:
                break
            self.line = str(queue.get())
            self.req = urllib2.Request(self.site + "/" + self.line)
            try:
                urllib2.urlopen(self.req,timeout=10)
            except urllib2.HTTPError as self.hr:
                if self.hr.code == 404:
                    print self.smode+": " + self.line.ljust(70,' '),
                    sys.stdout.write("\r")
            except urllib2.URLError as self.ur:
                printError("URL error:" + self.line.ljust(50,' ') + str(self.ur.args[0]).ljust(20,' '))
                exit()
            except ValueError as self.vr:
                pprintError("Value error:" + str(self.vr.args))
                exit()
            except:
                printWait("Unknown exception: exit...")
                exit()
            else:
                printResult(self.smode+": " + self.line.ljust(56,' ') + "[OK]".ljust(30,' '))
                try:
                	self.logging_file.writelog(self.smode+": " + self.line.ljust(50,' ') + "[OK]\n")
                except:
                	pass

# class Loading(threading.Thread):
#     def __init__(self,maxloading):
#         self.maxloading = maxloading
#         print self.maxloading
#         threading.Thread.__init__(self)
#         self.percent = 0
#     def run(self):
#         while queue.qsize()>0 and self.percent < 100:
#             self.percent = 100 * (self.maxloading - queue.qsize()) / self.maxloading
#             if self.percent > 100:
#                 self.percent = 100
#             print ''.ljust(60,' ')+ str(self.percent) + '%',
#             sys.stdout.write("\r")
#             time.sleep(2)
#         return
