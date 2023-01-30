#!/usr/bin/env python

'''
'''
import hashlib
from tkinter import *
import tkinter.filedialog
import requests
import os, time

def hash_b_i(bytesiter,hasher,ashexstr=False):
    for block in bytesiter:
        hasher.update(block)
    return (hasher.hexdigest() if ashexstr else hasher.digest())

def file_as_blockiter(afile, blocksize=65536):
    while afile:
        block = afile.read(blocksize)
        while len(block) > 0:
            yield block
            block = afile.read(blocksize)

print("start...")
fnamelst = ["test.txt"]
#fname = "test.txt"

#[(fname,hash_b_i(file_as_blockiter(open(fname,'rb')),hashlib.md5())) for fname in fnamelst]
#hash_b_i(file_as_blockiter(open(fname,'rb')),hashlib.md5())


#fe = "Kylin-Desktop-V10-Release-Build1-20200710-arm64.iso"
fe = "3M"

def cmd5(filename):
    #md5 = hashlib.md5()
    with open(filename,'rb') as f:
        for chunk in iter(lambda: f.read(2097152),b''):
            md5 = hashlib.md5()
            print(f.tell())
            md5.update(chunk)
            print(md5.hexdigest())
    print(md5.hexdigest())
    return md5.hexdigest()


#cmd5(fe)
'''
print('\n')
m5 = hashlib.md5()
with open(fe,'rb+') as f:
    m5.update(f.read())
print(m5.hexdigest())

'''

def upfile2(chunknumber,kuaidx,cchunksize,totalsize,identifier,filename,totalchunk,chunkmd5,chunk,username,userid):
    header = {}
    dd = {}    
    dd['chunkNumber'] = (None,chunknumber)
    dd['chunkSize'] = (None,kuaidx)
    dd['currentChunkSize'] = (None,cchunksize)
    dd['totalSize'] = (None,totalsize)
    dd['identifier'] = (None,identifier)
    dd['filename'] = (None,filename)
    dd['relativePath'] = (None,filename)
    dd['totalChunks'] = (None,totalchunk)
    dd['accept'] = (None,"*")
    dd['userId'] = (None,userid)
    dd['colonyId'] = (None,43)
    dd['toPath'] = (None,"/")
    dd['userHomeDir'] = (None,"/server/mnt/public1/home/" + username + "/" + username)
    #dd['userHomeDir'] = (None,"/tmp/" + username)
    dd['chunkMd5'] = (None,chunkmd5)
    dd['upfile'] = (None,chunk)
    dd['upfile'] = (filename,chunk)
    #url = "http://11.2.77.3:30089/portal-test/store/file/upload"
    url = "https://console.casjc.com/portal/store/file/upload"
    #r = requests.post(url,headers=header,files=dd)
    #print(r.content)
    #print(r.json()['code'])
    try:
        r = requests.post(url,headers=header,files=dd)
        if r.json()['code'] == 200:
            return 1
    #except:
     #       return None
    except requests.exceptions.Timeout as e:
        print('请求超时：'+str(e.message))
    except requests.exceptions.HTTPError as e:
        print('http请求错误:'+str(e.message))
    except requests.exceptions.ConnectionError:
        print('网卡断了')

root = Tk()

def cmd():
    #global e1
    username=e1.get()
    print(username)
    userid=e2.get()
    print(userid)
    fe = tkinter.filedialog.askopenfilename()
    p, filename = os.path.split(fe)
    print(filename)
    #print(fe)
    ffsize = os.path.getsize(fe)
    #print(ffsize)
    kuaidx = 2097152
    totalchunk = int(ffsize / kuaidx) + 1
    ident = cmd5(fe)
    with open(fe,'rb') as f:
        chunknumber = 0
        for chunk in iter(lambda: f.read(kuaidx),b''):
            chunknumber += 1
            md5 = hashlib.md5()
            #print(f.tell())
            md5.update(chunk)
            if len(chunk) < kuaidx:
                kuaisj = len(chunk)
            else:
                kuaisj = kuaidx
            print(len(chunk))
            chunkmd5 = md5.hexdigest()
            #print(chunkmd5)
            while True:
                if upfile2(chunknumber, kuaidx,kuaisj,ffsize,ident,filename,totalchunk,chunkmd5,chunk,username,userid):
                    break
                else:
                    time.sleep(1)
    e3.delete(0,END)
    e3.insert(0,'成功')
root.geometry('300x200')

l2 = Label(root,text="用户ID")
l2.pack()
e2 = Entry(root,text="输入")
e2.pack()
l1 = Label(root,text="用户名(先输入用户名)")
l1.pack()
e1 = Entry(root,text="ID")
e1.pack()
l3 = Label(root,text="状态")
l3.pack()
e3 = Entry(root,text="status")
e3.pack()

btn = Button(root,text="选择上传文件",command=cmd,fg="red",bg="blue")
btn.pack()
root.mainloop()
