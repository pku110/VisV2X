#coding=utf-8
import v2xConfig
import urllib2
import json
import sys
import time

def veSet(step):
    scIP = v2xConfig.scIP
    url = "http://%s/api/rpush/vip/%s" % (scIP,step)
    req = urllib2.Request(url)
    urllib2.urlopen(req)

def veGet():
    scIP = v2xConfig.scIP
    url = "http://%s/api/get/state" % scIP
    req = urllib2.Request(url)
    try:
        urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print '''
        %s
        %s
        %s
        %s
        ~~~~~~~~~~~~~~~~~~~~~~~~
        ''' % (e.code, e.reason, e.geturl(), e.read())

def getState():
    scIP = v2xConfig.scIP
    url = "http://%s/api/get/state" % scIP
    req = urllib2.Request(url)
    try:
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        res = json.loads(res)
        res = json.loads(res["get"])
    except:
        print "get error"
        res = None
    return res

if __name__ == '__main__':
    countdown = 1
    while 1 :
        #sys.stdout.write(str(getState())+"\r")
        res = getState()
        if str(res["step"]) == "3" or str(res["step"]) == "10":
            scIP = v2xConfig.scIP
            url = "http://%s/api/rpush/vip/0" % scIP
            req = urllib2.Request(url)
            urllib2.urlopen(req)
        if str(res["step"]) == "1" and str(res["step_countdown"]) == "2":
            veSet(9)

        print str(res["step"])+" "+str(res["step_countdown"])+" "+str(res["undercontrol"])
        sys.stdout.flush()
        time.sleep(1)
