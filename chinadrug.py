# !/user/bin/python
# coding: utf-8

import urllib
import urllib2
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import re

#get ID list
def getIDlst(keyword):
    header = {'Host':'www.chinadrugtrials.org.cn',
              'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0',
              'Referer':None
              }
    timeout = 5
    url = 'http://www.chinadrugtrials.org.cn/eap/clinicaltrials.searchlist'
    params = {'currentpage':'',
              'keywords':keyword,
              'pagesize':'20',
              'sort':'desc',
              'sort2':'desc',
              'rule':'CTR',
              'reg_no':'CTR'}
    ctrIDlst = {}
       
    req = urllib2.Request(url,urllib.urlencode(params),header)
    resp = urllib2.urlopen(req,None,timeout).read()
    
    reg = r'共<a style="color:#F00">(.+?)</a>页'
    pattern = re.compile(reg)
    pageNum = re.findall(pattern,resp)
    pageNum = int(''.join(pageNum).strip())
    
    for i in range(int(pageNum)):
        print i+1
        rssUrl = "http://www.chinadrugtrials.org.cn/eap/clinicaltrials.search.rss?"
        params['currentpage'] = i+1
        request = urllib2.Request(rssUrl,urllib.urlencode(params),header)
        response = urllib2.urlopen(request,None,timeout).read()
        soup = BeautifulSoup(response,'lxml')
        for child in soup.channel.children:
            if child.name == 'item':
                ctrIDlst[child.guid.string] = child.description.string
    return ctrIDlst

#download all word report
def downloadDOCFile(localPath):
    header = {'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
              'Host':"www.chinadrugtrials.org.cn",
              'Referer':"http://www.chinadrugtrials.org.cn/eap/clinicaltrials.searchlistdetail",
              'Cookie':"JSESSIONID=0000Xv3GZOZLnW7c90NkP66A_RB:-1; CNZZDATA1256895572=1238947871-1461716913-%7C1461746507"
              }
    timeout = 5
    url = 'http://www.chinadrugtrials.org.cn/exportdoc/clinicaltrials.searchlistdetail'

    params = {'ckm_id':'','ckm_index':''}
    for i in range(3097):
        print i+1
        params['ckm_index'] = i+1
        data = urllib.urlencode(params)
        req = urllib2.Request(url,data = data,headers = header)
        resp = urllib2.urlopen(req,None,timeout).read()
        reg = r'CTR(.+?)]'
        pattern = re.compile(reg)
        ctrID = re.findall(pattern,resp)
        filename = 'CTR'+ctrID[0]
        f =open(localPath+filename+'.doc','w')
        f.write(resp)
        f.close()

#download all html report
def downloadHTMLFile(localPath):
    header = {'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
              'Host':"www.chinadrugtrials.org.cn",
              'Referer':"http://www.chinadrugtrials.org.cn/eap/clinicaltrials.searchlist?a=a",
              'Cookie':"JSESSIONID=0000Xv3GZOZLnW7c90NkP66A_RB:-1; CNZZDATA1256895572=1238947871-1461716913-%7C1461746507"
              }
    timeout = 5
    url = 'http://www.chinadrugtrials.org.cn/eap/clinicaltrials.searchlistdetail'

    params = {'ckm_id':'','ckm_index':'','currentpage':'','pagesize':'20'}

    for i in range(3097):
        print i+1
        params['currentpage'] = i/20
        params['ckm_index'] = i+1
        data = urllib.urlencode(params)
        req = urllib2.Request(url,data = data,headers = header)
        resp = urllib2.urlopen(req,None,timeout).read()
        reg = r'CTR(.+?)详细信息'
        pattern = re.compile(reg)
        ctrID = re.findall(pattern,resp)
        filename = 'CTR'+ctrID[0]
        f = open(localPath+filename+'.html','w')
        f.write(resp)
        f.close()

def dictSave(dictlst,outfile):
    f = open(outfile,'w')
    for key in dictlst:
        f.write('\t'.join([key,dictlst[key]])+'\n')
    f.close()

if __name__=="__main__":
    localPath = '/home/ven/Puri/chinadrug/docfiles/'
    downloadDOCFile(localPath)

    # search ctrID according to keyword
    # example
    keyword = '糖尿病'
    ctrIDfile = '/home/ven/Puri/chinadrug/'+keyword+'.txt'
    dictSave(getIDlst(keyword),ctrIDfile)
