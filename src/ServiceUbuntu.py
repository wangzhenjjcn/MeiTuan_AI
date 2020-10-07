#!/usr/bin/env python
# -*- coding:utf-8 -*-
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import re
import time
import urllib
import lxml
import threading
import time
import requests
import base64
import json
import http.cookiejar as cookielib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import config
import codecs

class Application():
    # 这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        self.InitRuntime()
        d = threading.Thread(target=self.InitDriver)
        d.start()
        print("__init__end")


    def InitRuntime(self, event=None):
        print("Initing >>>>>>")
        self.InitDirs = []
        self.InitFiles = []
        self.CheckFiles=[]
        self.driver = None
        self.path = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.sys_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        print("Current Path:%s" % (self.path))
        self.configFilepath = self.path + "/config.ini"
        self.InitFiles.append(str(self.configFilepath))
        print("ConfigFileCheck Path:%s" % (self.configFilepath))
        self.driverFile = self.path + "/driver"
        self.CheckFiles.append(str(self.driverFile))
        print("DriverFile:%s" % (self.driverFile))
        self.tmpDir = self.path + "/tmp/"
        self.InitDirs.append(str(self.tmpDir))
        print("TmpPath:%s" % (str(self.tmpDir)))
        self.configPath = "默认设置"
        self.data_path = config.read_config(
            self.configFilepath, "默认设置", "save_path")
        self.userData_path = config.read_config(
            self.configFilepath, "默认设置", "userData_path")
         
        self.InitDirs.append(str(self.data_path))
        self.InitDirs.append(str(self.userData_path))
        self.initFileSystem()
        self.readConfigs()
        
    def initFileSystem(self, event=None):
        if self.InitDirs:
            for initdir_path in self.InitDirs:
                if initdir_path == None:
                    print("-----None:%s"%(initdir_path))
                    continue
                elif initdir_path == "":
                    continue
                elif not os.path.exists(initdir_path):
                    try:
                        print("%s is missing creat..." % (initdir_path))
                        print(initdir_path)
                        os.makedirs(initdir_path)
                        print("%s created!"%(initdir_path))
                        print("%s inited!" % (initdir_path))
                    except  Exception as e:
                        print(e)

        if self.InitFiles:
            for initFile_path in self.InitFiles:
                if initFile_path == None:
                    print("-----None:%s"%(initFile_path))
                    continue
                elif not os.path.exists(initdir_path):
                    try:
                        with open(initFile_path, 'w+', encoding='utf-8-sig') as f:
                            print("%s File Missing CreatingFile..."%(initFile_path))
                            f.flush()
                            f.close()
                    except  Exception as e:
                        print(e)

        if self.CheckFiles:
            for checkFile_path in self.CheckFiles:
                if checkFile_path == None:
                    print("-----None:%s"%(checkFile_path))
                    continue
                elif not os.path.exists(checkFile_path):
                    print("EEEEEEERRR:%s"% (checkFile_path))


        if (self.userData_path == None):
            self.userData_path = ""
        if os.path.exists(self.userData_path):
            print("userData_path inited")
        else:
            user_data_dir = self.userData_path
            if user_data_dir == None or user_data_dir == "" or not os.path.exists(user_data_dir):
                self.userData_path = self.tmpDir+"/" + \
                    str(time.time()).replace(".", "")+"/"
                user_data_dir = self.userData_path
            os.makedirs(user_data_dir)
        
    
    def readConfigs(self, event=None):
        self.defaultIndexLink=config.read_config_init(
            self.configFilepath, "默认设置", "default_index_link", "https://shangoue.meituan.com/")
        self.defaultHomepageLink=config.read_config_init(
            self.configFilepath, "默认设置", "default_homepage_link","https://shangoue.meituan.com/#menu#0")
        self.defaultMsg= config.read_config_init(
            self.configFilepath, "默认设置", "default_msg", "店家正在飞速赶来，请稍候～")
        self.repeatedlyMsg= config.read_config_init(
            self.configFilepath, "默认设置", "repeatedly_msg", "商家可能在忙，如未能及时回复请致电888-888888") 

    def InitDriver(self, event=None):
        if not os.path.exists(self.driverFile):
            return
        if self.driver != None:
            print("Already exist")
            self.loadCookie()
            print("cookie Loaded")
            self.driver.get(self.defaultHomepageLink)
            time.sleep(3)
            return
        self.driver = None
        try:
            chrome_options = Options()
            user_data_dir = self.userData_path
            if user_data_dir == None or user_data_dir == "" or not os.path.exists(user_data_dir):
                self.userData_path = self.tmpDir+"/" + \
                    str(time.time()).replace(".", "")+"/"
                user_data_dir = self.userData_path
            chrome_options.add_argument('--user-data-dir='+user_data_dir)
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--profile-directory=Default')
            chrome_options.add_argument("--incognito")
            chrome_options.add_argument("--disable-plugins-discovery")
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--enable-javascript')
            chrome_options.add_argument('--log-level=3')
            chrome_options.add_argument('--disable-popup-blocking')
            chrome_options.add_argument('-–single-process')
            chrome_options.add_argument('--ignore-ssl-errors')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            # chrome_options.binary_location = '/opt/google/chrome/chrome'
            self.driver = webdriver.Chrome(
                options=chrome_options, executable_path=self.driverFile)
            self.driver.set_page_load_timeout(8000)
            try:
                print("HTTPS-GET: %s"%(self.defaultIndexLink))
                self.driver.get(self.defaultIndexLink)
            except Exception as ee1:
                print("EER in HTTPS-GET: %s"%(self.defaultIndexLink))
                print(ee1)
            self.InitDriver()
        except Exception as e:
            if 'already in use' in str(e):
                self.userData_path = self.tmpDir+"/" + \
                    str(time.time()).replace(".", "")+"/"
                if self.driver != None:
                    self.driver.quit()
                    time.sleep(5)
                self.InitDriver()
            print("in getBrowser")
            print(e)
            return None
        pass

    def CheckNewMSG(self, event=None):
        try:
            pageSource = BeautifulSoup(self.driver.page_source, "lxml")
            try:
                sg_im_div=pageSource.find("div", id="sg-im")
                sg_im_entrance_div=sg_im_div.find("div", class_="wm-im-entrance")
                msg_num_b=sg_im_entrance_div.find("b") 
                self.newMsgNum=msg_num_b.text
                return True
            except Exception as e:
                return False            
            time.sleep(3)
            return True
        except Exception as e:
            return False
         
    def replyNewMsg(self,event=None):
        try:
            if not self.imOpened():
                self.openIM()
            try:
                pageSource = BeautifulSoup(self.driver.page_source, "lxml")
                sgImList=pageSource.find("div", id="sgImList")
                unrreadList = sgImList.findAll("div", class_="wm-im-item-wrapper cursor unread-item")
                if len(unrreadList) == 0:
                    print("lastRplyUserMsg")
                     
                    textareapath="//*[@id=\"sg-im-dialog\"]/div[2]/div[3]/div[3]/textarea"
                    self.driver.find_element_by_xpath(textareapath).send_keys(self.repeatedlyMsg)
                    sendbtnpath="//*[@id=\"sg-im-dialog\"]/div[2]/div[3]/div[4]/button"
                    sendbtn = self.driver.find_element_by_xpath(sendbtnpath)
                    webdriver.ActionChains(self.driver).move_to_element(sendbtn).click(sendbtn).perform()
                    self.closeIM()
                    return
                for unReadmsgDiv in unrreadList:
                    unReadmsgDivId=unReadmsgDiv.attrs['data-uid']
                    print("unread msg id :%s"%(unReadmsgDivId))
                    if "selected" not in unReadmsgDiv.attrs['class']:
                        msg=self.defaultMsg
                        unreadpath="//*[@data-uid=\"%s\"]"%(str(unReadmsgDivId))
                        msgtab = self.driver.find_element_by_xpath(unreadpath)
                        webdriver.ActionChains(self.driver).move_to_element(
                        msgtab).click(msgtab).perform()

                        print("clicked ")
                        textareapath="//*[@id=\"sg-im-dialog\"]/div[2]/div[3]/div[3]/textarea"
                        self.driver.find_element_by_xpath(textareapath).send_keys(self.defaultMsg)
                        sendbtnpath="//*[@id=\"sg-im-dialog\"]/div[2]/div[3]/div[4]/button"
                        sendbtn = self.driver.find_element_by_xpath(sendbtnpath)
                        webdriver.ActionChains(self.driver).move_to_element(sendbtn).click(sendbtn).perform()

                    else:
                        print("already select")
                    time.sleep(1)
                self.closeIM()
            except Exception as e2:
                print(e2)
                print("err close Im now")
                self.closeIM()
        except Exception as e:
            print(e)
 
    def openIM(self,event=None):
        try:
            # wm-im-entrance  
            imlinkxpath="//*[@id=\"sg-im\"]/div/div[1]/div[1]"
            imimg = self.driver.find_element_by_xpath(
                    imlinkxpath)
            webdriver.ActionChains(self.driver).move_to_element(
                    imimg).click(imimg).perform()
        except Exception as e:
            print(e)

    def closeIM(self,event=None):
       
        try:
            # wm-im-entrance  
            imlinkxpath="//*[@id=\"sg-im-dialog\"]/div[2]/div[1]/i[1]"
            imimg = self.driver.find_element_by_xpath(
                    imlinkxpath)
            webdriver.ActionChains(self.driver).move_to_element(
                    imimg).click(imimg).perform()
        except Exception as e:
            print(e)
        
    def imOpened(self,event=None):
        openstatus=False
        try:
            pageSource = BeautifulSoup(self.driver.page_source, "lxml")
            try:
                sg_im_div=pageSource.find("div", id="sg-im-dialog")
                if sg_im_div.attrs['style']==None:
                    openstatus=True
                else:
                    if "none" in sg_im_div.attrs['style']:
                        openstatus=False
                    else:
                        openstatus=True
            except Exception as e:
                print(e)      
        except Exception as e2:
            print(e2)
        msg="关闭"
        if openstatus:
            msg="打开"
        print("IM 状态：%s"%(msg))
        return openstatus
 
    def loadCookie(self, event=None):
        print("尝试读取登录历史->登录网站")
        cookieFileName = self.sys_path+"/"+'cookies.json'
        if not os.path.exists(cookieFileName):
            print("登录文件不存在，取消历史登录")
            with open(cookieFileName, 'w+', encoding='utf-8-sig') as f:
                print("Cookie File Missing CreatingFile...")
                f.flush()
                f.close()
            return False
        else:
            print("登录文件:[%s]，尝试历史登录" % (cookieFileName))
        with open(cookieFileName, 'r+', encoding='utf-8-sig') as f:
            data = f.read()
            if len(data) < 3 or data == "":
                print("JSON ERR:[%s]" % (data))
                return False
        listCookies = {}
        try:
            listCookies = json.loads(data)
            for cookie in listCookies:
                try:
                    self.driver.add_cookie(cookie)
                    print("cookie already load")
                except Exception as ed:
                    print(ed)
                    print(cookie)
                    pass
        except Exception as e:
            print("in listCookies")
            print(e)
            return False
        return True

    def mainloop(self,event=None): 
        print("start process")
        while self.RunningProcess:
            hasMsg=self.CheckNewMSG()
            if hasMsg:
                print("有%s条新消息啦！"%(self.newMsgNum))
                self.replyNewMsg()
            else:
                print("等待新消息～～～")
            
            time.sleep(2)

def str2Int(str):
    if str == None or str == "":
        return 0
    return int(str)

def getNoSpacestr(oldStr):
    newStr = ""
    firstSpace = True
    for c in oldStr:
        if c == " " and firstSpace:
            pass
        else:
            firstSpace=False
            newStr += c
    if str(newStr).endswith(" "):
        endStr = ""
        for d in newStr:
            endStr = d+endStr
            endStr = getNoSpacestr(endStr)
            newStr = ""
            for e in endStr:
                newStr = e+newStr
    return newStr


if __name__ == "__main__":
    app = Application()
    app.RunningProcess = True
    d = threading.Thread(target=app.InitDriver)
    e= threading.Thread(target=app.mainloop)
    d.start()
    time.sleep(15)
    e.start()
    pass