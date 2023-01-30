from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QLineEdit, QLCDNumber, QDial, QSlider, QLabel, QFormLayout, QLineEdit, QTextEdit, QFileDialog, QProgressBar, QRadioButton, QButtonGroup
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication, Qt, QBasicTimer, QThread, pyqtSignal

from random import randint
import hashlib
import requests
import os, time, sys, json



class dfThread(QThread):

        trigger = pyqtSignal(str)
        

        def __init__(self,ffsize,totalchunk,username,userid,file_up,filename_up, step):
            super().__init__()
            self.ffsize = ffsize
            self.totalchunk = totalchunk
            self.username = username
            self.userid = userid
            self.file_up = file_up
            #文件分片大小
            self.kuaidx = 2097152
            self.filename_up = filename_up
            self.step = step
            print(self.file_up)


        def run(self):
            #重写线程执行的run函数
            #触发自定义信号
            #for i in range(20):
                #time.sleep(1)
                # 通过自定义信号把待显示的字符串传递给槽函数
                #self.trigger.emit(str(i))
            print("123")
            self.trigger.emit(str(99))

        def runssss(self):
            print(1112222)
            with open(self.file_up,'rb') as f:
                chunknumber = 0
                chunknumber += 1
                print("当前块编号:" + str(chunknumber))
                #for chunk in iter(lambda: f.read(self.kuaidx),b''):
                for chunk in f.read(self.kuaidx):
                    if not f.read():
                        break
                    print(123)
                    chunknumber += 1
                    print("当前块编号:" + str(chunknumber))
                    if len(chunk) < self.kuaidx:
                        kuaisj = len(chunk)
                    else:
                        kuaisj = self.kuaidx
                    print(len(chunk))
                    while True:
                        if self.upfile3(chunknumber, kuaisj, chunk):
                            self.step = self.step + (100/self.totalchunk)
                            self.pbar.setValue(self.step)
                            break
                        else:
                            time.sleep(3)


        def upfile3(self,chunknumber, kuaisj, chunk):
            url = self.upfileurl
            header = {}
            header['Token'] = self.login_session
            dd = {}    
            dd['chunkNumber'] = (None,chunknumber)
            dd['chunkSize'] = (None,self.kuaidx)
            dd['currentChunkSize'] = (None,kuaisj)
            dd['totalSize'] = (None,self.totalsize)
            dd['identifier'] = (None,self.ident)
            dd['filename'] = (None,self.filename_up)
            dd['relativePath'] = (None,self.filename_up)
            dd['totalChunks'] = (None,self.totalchunk)
            dd['accept'] = (None,"*")
            dd['userId'] = (None,self.userid)
            dd['colonyId'] = (None,43)
            dd['toPath'] = (None,"/")
            dd['userHomeDir'] = (None, "/public1/" + "/home/" + self.username + "/" + self.username)
            dd['upfile'] = (self.filename_up,self.chunk)
            #print(dd)
            try:
                r = requests.post(url,headers=header,files=dd)
                print(r.content)
                if r.json()['code'] == 200:
                    return 1
                return None
            except requests.exceptions.Timeout as e:
                print('请求超时：'+str(e.message))
            except requests.exceptions.HTTPError as e:
                print('http请求错误:'+str(e.message))
            except requests.exceptions.ConnectionError:
                print('网卡断了')

        

class Example(QWidget):
        def __init__(self):
            super().__init__()
            #文件分片大小
            self.kuaidx = 2097152
            #self.kuaidx = 20971520
            self.tokenurl = "http://11.2.77.3:30089/portal-test/user/login/account"
            self.upfileurl = "http://11.2.77.3:30089/portal-test/store/file/upload"
            self.useridurl = "http://11.2.77.3:30089/portal-test/user/person/get"
            self.changepemurl = "http://11.2.77.3:30089/portal-test/store/file/merge"
            self.rbinfo = "内部"
            self.initUi3()
            self.ffsize = 123
            self.totalchunk = 123
            self.username = 123
            self.userid = 123
            self.file_up = 123
            self.filename_up =123
            self.step =123
            self.work = dfThread(self.ffsize,self.totalchunk,self.username,self.userid,self.file_up,self.filename_up, self.step)
            

            

        def initUi(self):
            lcd = QLCDNumber(self)
            lab = QLabel(self)
            #dial = QDial(self)
            dial = QSlider(self)
            
            
            self.setGeometry(300,300,350,250)
            self.setWindowTitle('忽然之间')

            lab.setGeometry(90,80,70,60)
            lcd.setGeometry(100,50,150,60)
            dial.setGeometry(120,120,100,100)

            dial.valueChanged.connect(lcd.display)
            lab.setText('a')
            self.show()

        def initUi2(self):
            self.setGeometry(300, 300, 350, 250)
            self.setWindowTitle('CASJC')
            self.lab = QLabel('方向',self)
            self.lab.setGeometry(150,100,50,50)
            self.show()

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

        def rbclicked(self):
            sender = self.sender()
            if sender == self.bg1:
                if self.bg1.checkedId() == 11:
                    self.tokenurl = "https://www.casjc.com/portal/user/login/account"
                    self.upfileurl = "https://console.casjc.com/portal/store/file/upload"
                    self.useridurl = "https://www.casjc.com/portal/user/person/get"
                    self.changepemurl = "https://console.casjc.com/portal/store/file/merge"
                    self.rbinfo = "线上"

                else:
                    self.tokenurl = "http://11.2.77.3:30089/portal-test/user/login/account"
                    self.upfileurl = "http://11.2.77.3:30089/portal-test/store/file/upload"
                    self.useridurl = "http://11.2.77.3:30089/portal-test/user/person/get"
                    self.changepemurl = "http://11.2.77.3:30089/portal-test/store/file/merge"
                

        def initUi4(self):
            self.setGeometry(300,300,300,200)
            self.setWindowTitle('CASJC')
            
            formlayout = QFormLayout()
            
            fileup = QLabel("文件上传")
            self.filebutton = QPushButton("选择文件",self)
                    
            self.filebutton.clicked.connect(self.selefile)       
            
            self.show()

        def selefile(self):
            self.file_up, self.bbb = QFileDialog.getOpenFileName(self,"打开文件",os.getcwd(),"All File(*)")
            p, self.filename_up = os.path.split(self.file_up)
            #print(self.filename_up)
            try:
                self.selefilenameup.setVisible(False)
            except:
                pass
            self.selefile = QLabel("选中文件")
            self.selefilename = QLabel(self.filename_up)

            self.jindu = QLabel("进度条")
            self.pbar = QProgressBar(self)
            self.pbar.setGeometry(30, 40, 200, 25)
            
            self.btn = QPushButton('开始上传', self)
            self.btn.move(40, 80)
            
            self.formlayout.addRow(self.selefile,self.selefilename)
            self.formlayout.addRow(self.jindu,self.pbar)
            self.formlayout.addRow(self.btn)
            self.btn.clicked.connect(self.cmd)

            self.timer = QBasicTimer()
            self.step = 0
            self.setGeometry(300, 300, 320, 200)
            

        def submitStore(self):
            print(self.nameLineEdit.text())
            print(self.introductionLineEdit.text())
            print(self.filename_up)


        def timerEvent(self, e):

            if self.step >= 100:
                self.step = 0
                self.pbar.setValue(self.step)
                self.timer.stop()
                self.btn.setText('完成')
                return
            #self.step = self.step+1
            #self.pbar.setValue(self.step)
        
        def cmd(self):
            print("do action")
            self.btn.setEnabled(False)
            if self.timer.isActive():
                self.timer.stop()
                self.btn.setText('开始')
            else:
                self.timer.start(100, self)
                self.btn.setText('上传中')
            print(self.username)
            self.userid = self.getuserId()
            print("文件名: " + self.filename_up)
            #文件大小
            self.ffsize = os.path.getsize(self.file_up)
            print("文件大小: " + str(self.ffsize))
            #文件分片块数
            self.totalchunk = int(self.ffsize / self.kuaidx) + 1
            print("文件块数: " + str(self.totalchunk))
            #self.work.start()

            #shangchuang = dfThread(self.ffsize,self.totalchunk,self.username,self.userid,self.file_up,self.filename_up, self.step)
            #shagnchuang.start()
            
            self.filerun(self.ffsize,self.totalchunk,self.username,self.userid)
            
            self.merge()
            print("ok")
            self.selefile.setVisible(False)
            self.selefilename.setVisible(False)
            self.pbar.setVisible(False)
            self.jindu.setVisible(False)
            self.btn.setVisible(False)
            self.selefilenameup = QLabel("文件:" + self.filename_up + " 上传完成")
            self.formlayout.addRow(self.selefilenameup)
            #self.btn.setEnabled(True)
            
        
        def execute(self):
            self.work.start()
            self.work.trigger.connect(self.display)

        def display(self):
            self.listWidget.addItem(str)

         
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
                        self.login_mess = '登录成功'
                        self.nameLabel.setVisible(False)
                        self.nameLineEdit.setVisible(False)
                        self.introductionLabel.setVisible(False)
                        self.introductionLineEdit.setVisible(False)
                        self.bt1.setVisible(False)
                        self.rb1.setVisible(False)
                        self.rb2.setVisible(False)
                        #self.bt2 = QPushButton('退出',self)
                        #self.bt2.setGeometry(200,200,30,20)
                        self.lab = QLabel(self.rbinfo,self)
                        self.fileup = QLabel("文件上传")
                        self.filebutton = QPushButton("选择文件",self)
                        self.colonyId = QLabel("colonyId")
                        self.mycolonyId = QLineEdit("43")
                        self.colonypath = QLabel("路径")
                        self.mycolonypath = QLineEdit("/public1")
                        self.formlayout.addRow(self.lab)
                        self.formlayout.addRow(self.colonyId,self.mycolonyId)
                        self.formlayout.addRow(self.colonypath,self.mycolonypath)
                        self.formlayout.addRow(self.fileup,self.filebutton)
                        self.filebutton.clicked.connect(self.selefile)
                        #self.bt2 = QPushButton('退出',self)
                        #self.bt2.setGeometry(155,150,60,40)
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

            #self.setLayout(self.formlayout)


        def getuserId(self):
            url = self.useridurl
            header = {}
            header["Authorization"] = self.login_session
            header['Token'] = self.login_session
            header['Cookie'] = "JSESSIONID=" + self.login_session
            r = requests.get(url, headers=header)
            #print(r.content)
            print(r.json()['data']['id'])
            return r.json()['data']['id']

        def filerun(self,ffsize,totalchunk,username,userid):
            #文件md5值
            self.ident = cmd5(self.file_up)
            with open(self.file_up,'rb') as f:
                chunknumber = 0
                for chunk in iter(lambda: f.read(self.kuaidx),b''):
                    chunknumber += 1
                    print("当前块编号:" + str(chunknumber))
                    #md5 = hashlib.md5()
                    #print(f.tell())
                    #md5.update(chunk)
                    if len(chunk) < self.kuaidx:
                        kuaisj = len(chunk)
                    else:
                        kuaisj = self.kuaidx
                    print(len(chunk))
                    #chunkmd5 = md5.hexdigest()
                    #print(chunkmd5)
                    while True:
                        if self.upfile2(chunknumber, kuaisj,ffsize,totalchunk,chunk,username,userid):
                            self.step = self.step + (100/self.totalchunk)
                            self.pbar.setValue(self.step)
                            break
                        else:
                            time.sleep(3)


        def upfile2(self,chunknumber,cchunksize,totalsize,totalchunk,chunk,username,userid):
            url = self.upfileurl
            header = {}
            header['Token'] = self.login_session
            dd = {}    
            dd['chunkNumber'] = (None,chunknumber)
            dd['chunkSize'] = (None,self.kuaidx)
            dd['currentChunkSize'] = (None,cchunksize)
            dd['totalSize'] = (None,totalsize)
            dd['identifier'] = (None,self.ident)
            dd['filename'] = (None,self.filename_up)
            dd['relativePath'] = (None,self.filename_up)
            dd['totalChunks'] = (None,totalchunk)
            dd['accept'] = (None,"*")
            dd['userId'] = (None,userid)
            dd['colonyId'] = (None,self.mycolonyId.text())
            dd['toPath'] = (None,"/")
            dd['userHomeDir'] = (None, self.mycolonypath.text())
            dd['upfile'] = (self.filename_up,chunk)
            #print(dd)
            try:
                r = requests.post(url,headers=header,files=dd)
                print(r.content)
                if r.json()['code'] == 200:
                    return 1
                return None
            except requests.exceptions.Timeout as e:
                print('请求超时：'+str(e.message))
            except requests.exceptions.HTTPError as e:
                print('http请求错误:'+str(e.message))
            except requests.exceptions.ConnectionError:
                print('网卡断了')

        def merge(self):
            url = self.changepemurl
            header = {}
            header['Token'] = self.login_session
            header['Content-Type'] = "application/json"
            dd = {}
            dd['colonyId'] = self.mycolonyId.text()
            dd['filename'] = self.filename_up
            dd['identifier'] = self.ident
            dd['isFolder'] = False
            dd['toPath'] = "/"
            dd['totalSize'] = self.ffsize
            dd['totalChunks'] = self.totalchunk
            dd['relativePath'] = self.filename_up
            dd['userHomeDir'] = self.mycolonypath.text()
            dd['userId'] = self.userid
            print(dd['userHomeDir'])
            print(header)
            r = requests.post(url,headers=header, data=json.dumps(dd))
            print(r.content)
            print(r.json())
        

def cmd5(filename):
    print('safsdf')
    md5 = hashlib.md5()
    with open(filename,'rb') as f:
        for chunk in iter(lambda: f.read(2097152),b''):
            #md5 = hashlib.md5()
            #print(f.tell())
            md5.update(chunk)
            #print(md5.hexdigest())
    print(md5.hexdigest())
    return md5.hexdigest()
        

if __name__ == "__main__":

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


