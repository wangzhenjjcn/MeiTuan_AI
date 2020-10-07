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
import ast
import http.cookiejar as cookielib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChain
from selenium.webdriver.common.keys import Keys
import config

try:
    from tkinter import *
except ImportError:  # Python 2.x
    PythonVersion = 2
    from Tkinter import *
    from tkFont import Font
    from ttk import *
    # Usage:showinfo/warning/error,askquestion/okcancel/yesno/retrycancel
    from tkMessageBox import *
    # Usage:f=tkFileDialog.askopenfilename(initialdir='E:/Python')
    #import tkFileDialog
    #import tkSimpleDialog
else:  # Python 3.x
    PythonVersion = 3
    from tkinter.font import Font
    from tkinter.ttk import *
    from tkinter.messagebox import *
    #import tkinter.filedialog as tkFileDialog
    # import tkinter.simpledialog as tkSimpleDialog    #askstring()


class Application_ui(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('美团用户信息管理系统')
        self.master.geometry('1187x664')
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.style.configure('RepSetting.TLabelframe',font=('宋体',9))
        self.RepSetting = LabelFrame(self.top, text='回复设置', style='RepSetting.TLabelframe')
        self.RepSetting.place(relx=0.209, rely=0.012, relwidth=0.776, relheight=0.977)

        self.style.configure('settingframe.TLabelframe',font=('宋体',9))
        self.settingframe = LabelFrame(self.top, text='设置', style='settingframe.TLabelframe')
        self.settingframe.place(relx=0.007, rely=0.012, relwidth=0.19, relheight=0.977)

        self.style.configure('Line1.TSeparator',background='#BFCDDB')
        self.Line1 = Separator(self.top, orient='vertical', style='Line1.TSeparator')
        self.Line1.place(relx=0.202, rely=0.012, relwidth=0.0008, relheight=0.976)

        self.List1Var = StringVar(value='List1')
        self.List1Font = Font(font=('宋体',9))
        self.List1 = Listbox(self.RepSetting, listvariable=self.List1Var, font=self.List1Font)
        self.List1.place(relx=0.096, rely=0.197, relwidth=0.87, relheight=0.746)

        self.Text1Var = StringVar(value='Text1')
        self.Text1 = Entry(self.RepSetting, text='Text1', textvariable=self.Text1Var, font=('宋体',9))
        self.Text1.place(relx=0.096, rely=0.037, relwidth=0.878, relheight=0.112)

        self.style.configure('Label2.TLabel',anchor='w', font=('宋体',9))
        self.Label2 = Label(self.RepSetting, text='回复记录：', style='Label2.TLabel')
        self.Label2.place(relx=0.017, rely=0.197, relwidth=0.079, relheight=0.039)

        self.style.configure('Label1.TLabel',anchor='w', font=('宋体',9))
        self.Label1 = Label(self.RepSetting, text='自动回复：', style='Label1.TLabel')
        self.Label1.place(relx=0.017, rely=0.037, relwidth=0.079, relheight=0.039)

        self.style.configure('StartCmd.TButton',font=('宋体',9))
        self.StartCmd = Button(self.settingframe, text='开始应答', command=self.StartCmd_Cmd, style='StartCmd.TButton')
        self.StartCmd.place(relx=0.178, rely=0.123, relwidth=0.573, relheight=0.063)

        self.style.configure('InitCmd.TButton',font=('宋体',9))
        self.InitCmd = Button(self.settingframe, text='初始化系统', command=self.InitCmd_Cmd, style='InitCmd.TButton')
        self.InitCmd.place(relx=0.178, rely=0.037, relwidth=0.573, relheight=0.063)

        self.InitCmd.bind(sequence='<Button-1>', func=self.handler_adaptor(self.handler, name="InitCmd",
                                                                           item=self.InitCmd, option="<Button-1>", item_type="cmd", log="初始化按钮点击", data=""))
        self.InitCmd.bind(sequence='<Button-3>', func=self.handler_adaptor(self.handler, name="InitCmd",
                                                                           item=self.InitCmd, option="<Button-3>", item_type="cmd", log="初始化按钮点击", data=""))
        self.StartCmd.bind(sequence='<Button-1>', func=self.handler_adaptor(self.handler, name="StartCmd",
                                                                            item=self.StartCmd, option="<Button-1>", item_type="cmd", log="采集按钮点击", data=""))
        self.InitCmd.bind(sequence='<Key-space>', func=self.handler_adaptor(self.handler, name="InitCmd",
                                                                            item=self.InitCmd, option="<Button-1>", item_type="cmd", log="初始化按钮空格", data=""))
        self.StartCmd.bind(sequence='<Key-space>', func=self.handler_adaptor(self.handler, name="StartCmd",
                                                                             item=self.StartCmd, option="<Button-1>", item_type="cmd", log="采集按钮空格", data=""))


class Application(Application_ui):
    # 这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        Application_ui.__init__(self, master)
        self.InitRuntime()
        d = threading.Thread(target=self.InitDriver)
        d.start()

    def handler_adaptor(self, fun,  **kwds):
        return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

    def handler(self, event, name, item, option, item_type, data, log):
        print("UI交互:控件["+name+"]类型["+item_type+"]操作["+option +
              "]数据["+str(data)+"]提示信息["+str(log)+"]")  # logmax 133
        if item_type == "cmd":
            if option == '<Button-1>':
                item.config(state="DISABLE")
            if option == '<Button-3>':
                self.loadCookie()

    def InitCmd_Cmd(self, event=None):
        # TODO, Please finish the function here!
        self.InitCmd.config(state="disable")
        
        d = threading.Thread(target=self.InitDriver)
        self.InitThread = d
        d.start()
        pass

    def StartCmd_Cmd(self, event=None):
        # TODO, Please finish the function here!
        self.StartCmd.config(state="disable")
        print("disable StartCmd_Cmd")
        self.RunningProcess = True
        e = threading.Thread(target=self.StartProcess)
        self.RunningThread = e
        e.start()
        pass

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
        self.InitFiles.append(self.configFilepath)
        print("ConfigFileCheck Path:%s" % (self.configFilepath))
        self.driverFile = self.path + "/driver.exe"
        self.CheckFiles.append(self.driverFile)
        print("DriverFile:%s" % (self.driverFile))
        self.tmpDir = self.path + "/tmp/"
        self.InitDirs.append(self.tmpDir)
        print("TmpPath:%s" % (self.tmpDir))
        self.configPath = "默认设置"
        self.data_path = config.read_config(
            self.configFilepath, "默认设置", "save_path")
        self.userData_path = config.read_config(
            self.configFilepath, "默认设置", "userData_path")
        self.InitDirs.append(self.data_path)
        self.InitDirs.append(self.userData_path)
        self.initFileSystem()

    def initFileSystem(self, event=None):
        if self.InitDirs:
            for initdir_path in self.InitDirs:
                if initdir_path == None:
                    print("-----None:%s"%(initdir_path))
                    continue
                elif not os.path.exists(initdir_path):
                    try:
                        print("%s missing creat..."%(initdir_path))
                        os.makedirs(initdir_path)
                        print("%s missing created!"%(initdir_path))
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
                        with open(initFile_path, 'w+', encoding='utf_8') as f:
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

        pass

    def InitUi(self, event=None):
        return

    def InitDriver(self, event=None):
        if not os.path.exists(self.driverFile):
            return
        if self.driver != None:
            print("Already exist")
            self.loadCookie()
            print("cookie Loaded")
            self.driver.get("https://shangoue.meituan.com/#menu#0")
            time.sleep(3)
            return
        self.driver = None
        try:
            chrome_options = webdriver.ChromeOptions()
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
            # chrome_options.binary_location = '/opt/google/chrome/chrome'
            self.driver = webdriver.Chrome(
                chrome_options=chrome_options, executable_path=self.driverFile)
            self.driver.set_page_load_timeout(8000)
            try:
                print("HTTPS-GET: https://shangoue.meituan.com/")
                self.driver.get("https://shangoue.meituan.com/")
            except Exception as ee1:
                print("EER in HTTPS-GET: https://shangoue.meituan.com/")
                print(ee1)

            self.InitCmd.config(state="NORMAL")
            self.StartCmd.config(state="NORMAL")
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

    def StartProcess(self, event=None):
        print("start process")
        while self.RunningProcess:
            self.StartCmd.config(state="disable")
            hasMsg=self.CheckNewMSG()
            if hasMsg:
                print("有%s条新消息啦！"%(self.newMsgNum))
                self.replyNewMsg()
            else:
                print("等待新消息～～～")
            self.StartCmd.config(state="NORMAL")
            time.sleep(2)


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
                unrreadList=sgImList.findAll("div", class_="wm-im-item-wrapper cursor unread-item")
                for unReadmsgDiv in unrreadList:
                    unReadmsgDivId=unReadmsgDiv.attrs['data-uid']
                    print("unread msg id :%s"%(unReadmsgDivId))
                    if "selected" not in unReadmsgDiv.attrs['class']:
                        unreadpath="//*[@data-uid=\"%s\"]"%(str(unReadmsgDivId))
                        msgtab = self.driver.find_element_by_xpath(unreadpath)
                        webdriver.ActionChains(self.driver).move_to_element(
                        msgtab).click(msgtab).perform()
                        time.sleep(2)
                        print("clicked ")
                        textareapath="//*[@id=\"sg-im-dialog\"]/div[2]/div[3]/div[3]/textarea"
                        msg=self.Text1.get()
                        self.driver.find_element_by_xpath(textareapath).send_keys(msg)
                        sendbtnpath="//*[@id=\"sg-im-dialog\"]/div[2]/div[3]/div[4]/button"
                        sendbtn = self.driver.find_element_by_xpath(sendbtnpath)
                        webdriver.ActionChains(self.driver).move_to_element(sendbtn).click(sendbtn).perform()
                        time.sleep(2)

                    else:
                        print("already select")
                    time.sleep(1)
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
    top = Tk()
    Application(top).mainloop()
    try:
        top.destroy()
    except:
        pass
