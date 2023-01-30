# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QLineEdit, QLCDNumber, QDial, QSlider, QLabel, QFormLayout, QLineEdit, QTextEdit, QFileDialog, QProgressBar, QRadioButton, QButtonGroup
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication, Qt, QBasicTimer, QThread, pyqtSignal

from random import randint
import hashlib
import requests
import os, time, sys, json

class MyMainForm(QWidget):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.tokenurl = "http://11.2.77.3:30089/portal-test/user/login/account"
        self.upfileurl = "http://11.2.77.3:30089/portal-test/store/file/upload"
        self.useridurl = "http://11.2.77.3:30089/portal-test/store/store/colonyList"
        self.changepemurl = "http://11.2.77.3:30089/portal-test/store/file/merge"
        self.rbinfo = "内部"
        self.initUi3()
        


    def initUi3(self):
            self.setGeometry(300,300,300,200)
            self.setWindowTitle('CASJC')
            
            self.formlayout = QFormLayout()

            self.rb1 = QRadioButton('线上',self)
            self.rb2 = QRadioButton('内部',self)
            self.rb2.setChecked(True)

            self.bg1 = QButtonGroup(self)
            self.bg1.addButton(self.rb1,11)
            self.bg1.addButton(self.rb2,22)
            
            self.info1 = ""
            self.info2 = ""

            self.bg1.buttonClicked.connect(self.rbclicked)
            
            self.nameLabel = QLabel("账号")
            self.nameLineEdit = QLineEdit("")
            
            self.introductionLabel = QLabel("密码")
            self.introductionLineEdit = QLineEdit("")
            #self.introductionLineEdit = QTextEdit("")

            self.bt1 = QPushButton('登录',self)
            self.bt1.setGeometry(115,150,70,30)
            self.bt1.setToolTip('登录先进云计算平台')

            self.formlayout.addRow(self.rb1,self.rb2)
            self.formlayout.addRow(self.nameLabel,self.nameLineEdit)
            self.formlayout.addRow(self.introductionLabel,self.introductionLineEdit)
            #formlayout.addRow(fileup,self.filebutton)
            self.formlayout.addRow(self.bt1)
            self.setLayout(self.formlayout)

            self.bt1.clicked.connect(self.Casjc_login)
           
            self.show()

    def Casjc_login(self): 
            self.username = self.nameLineEdit.text()
            #print(self.introductionLineEdit.text())
            url = self.tokenurl
            header = {}
            header['Content-Type'] = "application/json"
            data = {}
            data["account"] = self.nameLineEdit.text()
            data["password"] = self.introductionLineEdit.text()
            data["rememberMe"] = False
            data["origin"] = 0
            try:
                r = requests.post(url, headers=header, data=json.dumps(data))
                if r.status_code == 200:
                    if r.json()['code'] == 200:
                        print(r.json()['data'])
                        self.login_session = r.json()['data']
                        self.getuserId()
                        self.login_mess = '登录成功'
                        self.nameLabel.setVisible(False)
                        self.nameLineEdit.setVisible(False)
                        self.introductionLabel.setVisible(False)
                        self.introductionLineEdit.setVisible(False)
                        self.bt1.setVisible(False)
                        self.rb1.setVisible(False)
                        self.rb2.setVisible(False)
                        self.lab = QLabel(self.rbinfo,self)
                        self.fileup = QLabel("文件上传")
                        self.filebutton = QPushButton("选择文件",self)
                        self.colonyId = QLabel("colonyId")
                        self.mycolonyId = QLineEdit(self.store_colonyid)
                        self.mycolonyId.setEnabled(False)
                        self.colonypath = QLabel("路径")
                        self.mycolonypath = QLineEdit(self.store_path)
                        self.mycolonypath.setEnabled(False)
                        self.formlayout.addRow(self.lab)
                        self.formlayout.addRow(self.colonyId,self.mycolonyId)
                        self.formlayout.addRow(self.colonypath,self.mycolonypath)
                        self.formlayout.addRow(self.fileup,self.filebutton)
                        self.filebutton.clicked.connect(self.selefile)
                    else:
                        print('登录认证信息错误')
                        self.login_mess = '登录认证信息错误'
                else:
                    print('登录异常')
                    self.login_mess = '登录异常'
            except requests.exceptions.ConnectionError:
                print("网络异常无法连接服务器")
                self.login_mess = '网络异常无法连接服务器'
            except requests.exceptions.MissingSchema:
                print('请求的Url地址有误')
                self.login_mess = '请求的Url地址有误'
            except requests.exceptions.Timeout as e:
                print('请求超时：' + str(e.message))
                self.login_mess = '请求超时'
            except requests.exceptions.HTTPError as e:
                print('http请求错误:' + str(e.message))
                self.login_mess = 'http请求错误'
            reply = QMessageBox.information(self, "登录提示信息", self.login_mess, QMessageBox.Yes)
            self.getuserId()

            #self.setLayout(self.formlayout)

    def getuserId(self):
            url = self.useridurl
            header = {}
            header["Authorization"] = self.login_session
            header['Token'] = self.login_session
            header['Cookie'] = "JSESSIONID=" + self.login_session
            r = requests.get(url, headers=header)
            self.store_userid = r.json()['data'][0]['userId']
            self.store_colonyid = str(r.json()['data'][0]['colonyId'])
            self.store_path = r.json()['data'][0]['path']
            return None


        
    def selefile(self):
            self.file_up, self.bbb = QFileDialog.getOpenFileName(self,"打开文件",os.getcwd(),"All File(*)")
            p, self.filename_up = os.path.split(self.file_up)
            try:
                self.selefilenameup.setVisible(False)
            except:
                pass
            
            self.selefile = QLabel("选中文件")
            self.selefilename = QLabel(self.filename_up)

            self.jindu = QLabel("进度条")
            #self.pbar = QProgressBar(self)
            #self.pbar.setGeometry(30, 40, 200, 25)
            
            self.btn = QPushButton('开始上传', self)
            self.btn.move(40, 80)
            
            self.formlayout.addRow(self.selefile,self.selefilename)
            #self.formlayout.addRow(self.jindu,self.pbar)
            self.formlayout.addRow(self.btn)
            self.btn.clicked.connect(self.execute)

            self.timer = QBasicTimer()
            self.step = 0
            self.setGeometry(300, 300, 320, 200)

    
    def rbclicked(self):
            sender = self.sender()
            if sender == self.bg1:
                if self.bg1.checkedId() == 11:
                    self.tokenurl = "https://www.casjc.com/portal/user/login/account"
                    self.upfileurl = "https://console.casjc.com/portal/store/file/upload"
                    self.useridurl = "https://console.casjc.com/portal/store/store/colonyList"
                    self.changepemurl = "https://console.casjc.com/portal/store/file/merge"
                    self.rbinfo = "线上"

                else:
                    self.tokenurl = "http://11.2.77.3:30089/portal-test/user/login/account"
                    self.upfileurl = "http://11.2.77.3:30089/portal-test/store/file/upload"
                    self.useridurl = "http://11.2.77.3:30089/portal-test/store/store/colonyList"
                    self.changepemurl = "http://11.2.77.3:30089/portal-test/store/file/merge"

    def timerEvent(self, e):
            global step
            if step >= 100:
                step = 0
                self.pbar.setValue(step)
                self.timer.stop()
                self.btn.setText('完成')
                return

    def execute(self):
            self.btn.setEnabled(False)
            '''
            if self.timer.isActive():
                self.timer.stop()
                self.btn.setText('开始')
            else:
                self.timer.start(100, self)
                self.btn.setText('上传中')
            '''
            aaa = 123
            self.work = WorkThread()
            
            # 启动线程
            myll = [self.login_session,self.filename_up,self.file_up,self.store_colonyid,self.store_path,self.username,self.store_userid,self.btn,self.changepemurl,self.upfileurl,self.btn]
            self.work.setval(myll)
            # 线程自定义信号连接的槽函数
            '''
            self.work.trigger.connect(self.display)
            
            self.selefile.setVisible(False)
            self.selefilename.setVisible(False)
            self.pbar.setVisible(False)
            self.jindu.setVisible(False)
            self.btn.setVisible(False)
            self.selefilenameup = QLabel("文件:" + self.filename_up + " 上传完成")
            self.formlayout.addRow(self.selefilenameup)
            '''

    def display(self,val):
            print("start" + val)
            # 由于自定义信号时自动传递一个字符串参数，所以在这个槽函数中要接受一个参数
            self.listWidget.addItem(str)

class WorkThread(QThread):
    # 自定义信号对象。参数str就代表这个信号可以传一个字符串
    trigger = pyqtSignal(str)

    def __int__(self):
        # 初始化函数
        super(WorkThread, self).__init__()



    def setval(self,*val):            
        self.session = val[0][0]
        self.filename = val[0][1]
        self.fullfilename = val[0][2]
        self.colonyId = val[0][3]
        self.colonyPath = val[0][4]
        self.username = val[0][5]
        self.userid = val[0][6]
        self.kuaidx = 2097152
        md5 = hashlib.md5()
        with open(self.fullfilename,'rb') as f:
            for chunk in iter(lambda: f.read(self.kuaidx),b''):
                md5.update(chunk)
                #print(md5.hexdigest())
        self.ident = md5.hexdigest()
        self.step = 0
        self.start()
        self.btnname = val[0][7]
        self.upurl = val[0][9]
        self.meurl = val[0][8]
        #self.trigger.emit("dog")

               
    def run(self):
        #print(self.upurl)
        #print(self.meurl)
        #print(self.colonyId)
        #print(self.colonyPath)
        #触发自定义信号
        self.btnname.setText('上传中')
        
        for i in range(1):
            # 通过自定义信号把待显示的字符串传递给槽函数
            #self.trigger.emit(str(i))
            header = {}
            header['Token'] = self.session
            dd = {}  
            #文件大小
            ffsize = os.path.getsize(self.fullfilename)
            print("文件大小: " + str(ffsize))
            #文件分片块数
            totalchunk = int(ffsize / self.kuaidx)
            if ffsize % self.kuaidx:
                totalchunk += 1
            print("文件块数: " + str(totalchunk))
            dd['chunkSize'] = (None,self.kuaidx)
            dd['totalSize'] = (None,ffsize)
            dd['identifier'] = (None,self.ident)
            dd['filename'] = (None,self.filename)
            dd['relativePath'] = (None,self.filename)
            dd['totalChunks'] = (None,totalchunk)
            dd['accept'] = (None,"*")
            dd['userId'] = (None,self.userid)
            dd['colonyId'] = (None,self.colonyId)
            dd['toPath'] = (None,"/")
            dd['userHomeDir'] = (None, self.colonyPath)
            with open(self.fullfilename,'rb') as f:
                chunknumber = 0
                for chunk in iter(lambda: f.read(self.kuaidx),b''):
                    chunknumber += 1
                    #print("当前块编号:" + str(chunknumber))
                    if len(chunk) < self.kuaidx:
                        kuaisj = len(chunk)
                    else:
                        kuaisj = self.kuaidx
                    #print(kuaisj)
                    dd['chunkNumber'] = (None,chunknumber)            
                    dd['currentChunkSize'] = (None,kuaisj)           
                    dd['upfile'] = (self.filename,chunk)
                    while True:
                        try:
                            r = requests.post(self.upurl,headers=header,files=dd)
                            #print(r.content)
                            if r.json()['code'] == 200:
                                self.step = self.step + (100/totalchunk)
                                self.btnname.setText('上传中 (' + str(int(self.step))+ ' %)')
                                break
                        except requests.exceptions.Timeout as e:
                            print('请求超时：'+str(e.message))
                        except requests.exceptions.HTTPError as e:
                            print('http请求错误:'+str(e.message))
                        except requests.exceptions.ConnectionError:
                            print('网卡断了')

            header2 = {}
            header2['Token'] = self.session
            header2['Content-Type'] = "application/json"
            dd2 = {}
            dd2['colonyId'] = self.colonyId
            dd2['filename'] = self.filename
            dd2['identifier'] = self.ident
            dd2['isFolder'] = False
            dd2['toPath'] = "/"
            dd2['totalSize'] = ffsize
            dd2['totalChunks'] = totalchunk
            dd2['relativePath'] = self.filename
            dd2['userHomeDir'] = self.colonyPath
            dd2['userId'] = self.userid
            r = requests.post(self.meurl,headers=header2, data=json.dumps(dd2))
            print(r.content)
            self.btnname.setText('完成')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())
