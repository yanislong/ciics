#!/usr/bin/env python3
#-*-coding=utf-8-*-

from flask import Flask, request, send_from_directory, url_for, session, escape
from flask import render_template, make_response, abort, redirect, Response
#from werkzeug import secure_filename
from flask import jsonify
import os, random, json, sys, pymysql, subprocess, base64, binascii
sys.path.append(os.getcwd() + '/run_test')
sys.path.append(os.getcwd() + '/zzqf')
sys.path.append(os.getcwd() + '/run_test/excel')
sys.path.append(os.getcwd() + '/run_test/lhlmysql')
sys.path.append(os.getcwd() + '/run_test/integrateTest/user')
try:
    import myrule
except ModuleNotFoundError:
    pass

from run_test.lhlmysql.lhlsql import lhlSql
from decimal import Decimal
from run_test import autoInter, importInter
import socket
import config

UPLOAD_FOLDER = "./run_test/excel/"
ALLOWED_EXTENSIONS = set(['json','txt','jpeg','xlsx','xls','gz','png'])

app = Flask(__name__)

def myfun():
    return "abc"

#jinja2模板调用导入函数
app.jinja_env.globals.update(myfun=myfun)
#jinja2模板调用导入包
app.jinja_env.globals.update(json=json)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 1024
app.config['JSON_AS_ASCII'] = False
app.secret_key = os.urandom(12)


@app.route('/music', methods=["GET"])
def hw0414():
    return render_template("music.mp3")

@app.route('/', methods=["GET"])
def hw():
    res = (config.name, config.bugurl, config.music, config.saying)
    return render_template("index.html", result=(res,))

@app.route('/login', methods=['GET','POST'])
def login():
    if session.get('username') == "lihailong":
        return redirect(url_for('index'))
    return """<form method='get'>
    <p><input type='text' name=username></p>
    <p><input type='submit' value=login></p>
    </form>"""


@app.route('/shelllog', methods=['GET','POST'])
def test01():
    kong = None
    if request.method == "GET":
        get_inter = request.args.get("interface")
        get_result = request.args.get("result")
        get_id = request.args.get("myid")
        try:
            get_page = int(request.args.get("page"))
        except:
            get_page = 1
    if get_page >= 1:
        temp_page = (get_page - 1) * 20
    else:
        temp_page = 0
    if isinstance(get_inter,type(kong)):
        get_inter = ""
    if isinstance(get_id,type(kong)):
        get_id = ""
    if isinstance(get_result,type(kong)):
        get_result = ""
    mydata = lhlSql()
    webbodydata = mydata.getShellRespondList(get_inter, get_result, get_id, temp_page)
    webtotalnumber = mydata.getTotalShellRespondNumber(get_inter,get_result)
    webnamedata = mydata.getShellRespondName()
    webtotalpage = int(webtotalnumber / 20) + 1
    intername = mydata.getInterfaceRespondName()
    return render_template('shell.html', result=(webbodydata,webtotalnumber,webtotalpage,intername,webnamedata,config.music))

@app.route('/shelllist')
def test02():
    return render_template("shelllist.html", result=())

@app.route('/runanjian', methods=['GET','POST'])
def runanjian():
    subprocess.Popen('python3 /root/dockerdir/myPerformance/GKJY-TEST/zzqf/tpa/tpa_anjianbiangeng.py', shell=True)

@app.route('/runpay', methods=['GET','POST'])
def runpay():
    subprocess.Popen('python3 /root/dockerdir/myPerformance/GKJY-TEST/zzqf/pay/pay.py', shell=True)
    return render_template('shelllist.html', result=())

#待请求接口中的上传文件
@app.route('/downloadfile/', methods=['GET', 'POST'])
def downloadfile():
    if request.method == 'GET':
        #fullfilename = request.args.get('filename')
        fullfilename = './templates/file/interfacedata.xlsx'
        fullfilenamelist = fullfilename.split('/')
        filename = fullfilenamelist[-1]
        filepath = fullfilename.replace('/%s'%filename, '')
        #普通下载
        # response = make_response(send_from_directory(filepath, filename, as_attachment=True))
        # response.headers["Content-Disposition"] = "attachment; filename={}".format(filepath.encode().decode('latin-1'))
        #return send_from_directory(filepath, filename, as_attachment=True)
        #流式读取
        def send_file():
            store_path = fullfilename
            with open(store_path, 'rb') as targetfile:
                while 1:
                    data = targetfile.read(20 * 1024 * 1024)   # 每次读取20M
                    if not data:
                        break
                    yield data
        
        response = Response(send_file(), content_type='application/octet-stream')
        response.headers["Content-disposition"] = 'attachment; filename=%s' % filename   # 如果不加上这行代码，导致下图的问题
        return  response

@app.route('/collvalue', methods=['GET'])
def coll():
    mydata = lhlSql()
    res = mydata.getCollValue()
    return render_template('collvalue.html', result=(res,))

@app.route('/rule', methods=['GET'])
def rule():
    try:
        print(myrule.rule)
    except NameError:
        return render_template('test.html', result=())
    return render_template('rule.html', result=(myrule.rule,))

@app.route('/integrate', methods=["POST","GET"])
def integr():
    if request.method == "POST":
        try:
            get_name = request.get_data()
        except KeyError:
            get_name = "hello world"
        get_name = get_name.decode('utf-8')
        get_name = get_name.split(',')
        print(get_name)
        for i in get_name:
            doc = 'python3 ./run_test/integrateTest/' + i + '.py'
            print(doc)
            p = subprocess.Popen(doc, shell=True)
            out,err=p.communicate(timeout=15)
        return jsonify({"msg": {"out": out,"err": err}, "status": 0})
    elif request.method == "GET":
        return render_template('integrate.html', result=())

@app.route('/addInterface', methods=['GET','POST'])
def qianyun3():
    if request.method == "POST":
        try:
            #get_name = request.get_data()
            get_mode = request.form['imode']
            get_desc = request.form['idesc']
            get_addr = request.form['iaddr']
            get_header = request.form['iheader']
            get_param = request.form['iparam']
            get_option = request.form['ioption']
            get_author = request.form['iauthor']
            get_result = request.form['iresult']
            get_userpwd = request.form['iuserpwd']
            mydata = lhlSql()
            mydata.insertInterface(get_mode,get_addr,get_header,get_param,get_option,get_author,get_desc,get_result,get_userpwd)
        except TypeError:
            get_mode = ""
            get_desc = ""
            get_addr = ""
            get_header = ""
            get_parama = ""
            get_option = ""
            get_author = ""
            get_result = ""
            get_userpwd = ""
    return qianyun4()

@app.route('/updateInterface', methods=['GET','POST'])
def updateInter():
    if request.method == "POST":
        try:
            #get_name = request.get_data()
            get_mode = request.form['imode']
            get_desc = request.form['idesc']
            get_addr = request.form['iaddr']
            get_header = request.form['iheader']
            get_param = request.form['iparam']
            get_option = request.form['ioption']
            get_author = request.form['iauthor']
            get_result = request.form['iresult']
            get_userpwd = request.form['iuserpwd']
            get_id = request.form['iid']
            mydata = lhlSql()
            mydata.UpdateInterfaceWithId(get_mode,get_addr,get_header,get_param,get_option,get_author,get_desc,get_result,get_userpwd,get_id)
        except TypeError:
            get_mode = ""
            get_desc = ""
            get_addr = ""
            get_header = ""
            get_parama = ""
            get_option = ""
            get_author = ""
            get_result = ""
            get_userpwd = ""
            get_id = ""
    return qianyun4()

@app.route('/runtest', methods=['GET','POST'])
def runtest():
    subprocess.Popen('python3 ./run_test/autoInter.py', shell=True)
    return qianyun4()

@app.route('/interfaceList', methods=['GET','POST'])
def qianyun4():
    kong = None
    get_inter = request.args.get("interface")
    get_author = request.args.get("author")
    try:
        get_page = int(request.args.get("page"))
    except:
        get_page = 1
    if get_page >= 1:
        temp_page = (get_page - 1) * 20
    else:
        temp_page = 0
    if isinstance(get_inter,type(kong)):
        get_inter = ""
    if isinstance(get_author,type(kong)):
        get_author = ""
    mydata = lhlSql()
    webbodydata = mydata.getInterfaceList(get_inter, get_author, temp_page)
    webtotalnumber = mydata.getTotalInterfaceNumber(get_inter, get_author)
    webnamedata = mydata.getInterfaceInfoName()
    webnamedataauthor = mydata.getInterfaceAuthor()
    webtotalpage = int(webtotalnumber / 20) + 1
    intername = mydata.getInterfaceInfoName()
#    print(webbodydata)
    return render_template('interfacelist.html', result=(webbodydata,webtotalnumber,webtotalpage,intername,webnamedata,webnamedataauthor,config.intermode,config.option,config.author,config.music))

@app.route('/delinterface', methods=['GET','POST'])
def delinter():
    if request.method == "GET":
        try:
            get_id = request.args.get("iid")
        except KeyError:
            get_id = ""
        try:
            get_rd = request.args.get("rid")
        except KeyError:
            get_rd = ""
        print(get_id)
        print(get_rd)
        if get_id == "" or get_id == None:
            myrun = autoInter.lhl()
            myrun.oneTest(get_rd)
            return qianyun4()
        elif get_rd == "" or get_rd == None:
            mydata = lhlSql()
            mydata.DelInterface(get_id)
            return qianyun4()
        else:
            return qianyun4()

@app.route('/interfaceRespondList', methods=['GET','POST'])
def qianyun5():
    kong = None
    if request.method == "GET":
        get_inter = request.args.get("interface")
        get_result = request.args.get("result")
        get_id = request.args.get("myid")
        print(get_id)
        print("*****")
        try:
            get_page = int(request.args.get("page"))
        except:
            get_page = 1
    if get_page >= 1:
        temp_page = (get_page - 1) * 20
    else:
        temp_page = 0
    if isinstance(get_inter,type(kong)):
        get_inter = ""
    if isinstance(get_id,type(kong)):
        get_id = ""
    if isinstance(get_result,type(kong)):
        get_result = ""
    mydata = lhlSql()
    webbodydata = mydata.getInterfaceRespondList(get_inter, get_result, get_id, temp_page)
    webtotalnumber = mydata.getTotalInterfaceRespondNumber(get_inter,get_result)
    webnamedata = mydata.getInterfaceRespondName()
    webtotalpage = int(webtotalnumber / 20) + 1
    intername = mydata.getInterfaceRespondName()
    return render_template('interfacerespondlist.html', result=(webbodydata,webtotalnumber,webtotalpage,intername,webnamedata,config.music))

@app.route('/qianyunPOST')
def qianyunpost():
    if request.method == "GET":
        get_inter = request.args.get("interface")
        get_id = request.args.get("id")
        get_page = request.args.get("page")
    else:
        get_inter = ""
        get_id = ""
        get_page = 1
    con = pymysql.connect('10.0.114.44','root','root','portaltest')
    sql_time = []
    cursor = con.cursor()
    try:
        get_page = int(get_page)
    except:
        get_page = 1
    sql = "select * from qianyun_post where content like '%{0}%' and id like '%{1}%' limit {2},20".format(get_inter,get_id,(get_page-1)*20)
    cursor.execute(sql)
    seldata = cursor.fetchall()
    sql2 = "select count(*) from qianyun_post where content like '%{0}%' and id like '%{1}%'".format(get_inter,get_id)
    cursor.execute(sql2)
    total = cursor.fetchall()
    if not total:
        total = 1.0
    totalPage = str(round(int(total[0][0]) / int(20),0))[:-2]
    sql_dns_time = "select sum(dns_time) from qianyun_post where content like '%{0}%' and id like '%{1}%'".format(get_inter,get_id)
    cursor.execute(sql_dns_time)
    dns_time = cursor.fetchall()
    #sql_time.append(dns_time[0][0])
    sql_conn_time = "select sum(conn_time) from qianyun_post where content like '%{0}%' and id like '%{1}%'".format(get_inter,get_id)
    cursor.execute(sql_conn_time)
    conn_time = cursor.fetchall()
    try:
        sql_time.append(round(conn_time[0][0]/total[0][0],8))
    except:
        sql_time.append(1)
    sql_startData_time = "select sum(startData_time) from qianyun_post where content like '%{0}%' and id like '%{1}%'".format(get_inter,get_id)
    cursor.execute(sql_startData_time)
    startData_time = cursor.fetchall()
    try:
        sql_time.append(round(startData_time[0][0]/total[0][0],8))
    except:
        sql_time.append(1)
    sql_total_time = "select sum(total_time) from qianyun_post where content like '%{0}%' and id like '%{1}%'".format(get_inter,get_id)
    cursor.execute(sql_total_time)
    total_time = cursor.fetchall()
    try:
        sql_time.append(round((total_time[0][0]/total[0][0]),8))
    except:
        sql_time.append(1)
    sql_updata = "select sum(updata) from qianyun_post where content like '%{0}%' and id like '%{1}%'".format(get_inter,get_id)
    cursor.execute(sql_updata)
    updata = cursor.fetchall()
    sql_time.append(updata[0][0])
    sql_downdata = "select sum(downdata) from qianyun_post where content like '%{0}%' and id like '%{1}%'".format(get_inter,get_id)
    cursor.execute(sql_downdata)
    downdata = cursor.fetchall()
    sql_time.append(downdata[0][0])
    print(sql_time)
    sql_name = "select distinct content from qianyun_post"
    cursor.execute(sql_name)
    inter_name = cursor.fetchall()
    cursor.close()
    con.close()
    return render_template('qianyunPOST.html', result=(seldata,total,sql_time,totalPage,inter_name,get_page))

def allowed_file(filename):
    return "." in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/passwd/<int:age>')
def get_p(age):
    if age>100:
        return "Username: %d" % age
    else:
        return "input error"

@app.route('/uploadfile', methods=['POST'])
def upload_file():
    f = request.files['myf']
    print(f)
    if f and allowed_file(f.filename):
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        #subprocess.Popen('python3 /root/lhl/myPerformance/GKJY-TEST/run_test/importInter.py', shell=True)
        return importInter.readInter()
        #return render_template('interfacelist.html', result=())
    else:
        return render_template('error.html', result=())

@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/deal_request', methods=['GET','POST'])
def deal_request():
    if request.method == "GET":
        get_q = request.args.get("q","")
        return render_template('result.html', result=get_q)
    elif request.method == "POST":
        post_q = request.form["q"]
        return render_template('result.html', result=post_q)


@app.route('/qianyunGET')
def qianyun():
    if request.method == "GET":
        get_inter = request.args.get("interface")
        try:
            get_page = int(request.args.get("page"))
        except:
            get_page = 1
        if get_page >= 1:
            get_page = (get_page - 1) * 10
        else:
            get_page = 0
        if get_inter == None:
            get_inter = ""
        mydata = lhlSql()
        webbodydata = mydata.getTimeInfo(get_inter, get_page)
        webavgdata = mydata.getTimeList(get_inter)
        webnamedata = mydata.getInterfaceName()
        webtotalnumber = mydata.getTotalNumber(get_inter)
        temp = []
        temp2 = []
        for i in webavgdata[0]:
            try:
                num = round(Decimal(i/webtotalnumber),6)
                temp.append(num)
            except TypeError:
                return render_template('qianyunGET.html', result=(webbodydata,webtotalnumber,1,"",webnamedata))
        temp2.append((temp))
        webtotalpage = int(webtotalnumber / 20)
        return render_template('qianyunGET.html', result=(webbodydata,webtotalnumber,webtotalpage,temp2,webnamedata))
    return None

@app.route('/test')
def mytest():
    return render_template('test.html')

@app.route('/mytest', methods=['GET', 'POST'])
def mytest2():
    if request.method == "POST":
        message = request.get_data()
        message = json.loads(message.decode('utf-8'))
        mydata = lhlSql()
        temp = mydata.getIdInterface(message['editId'])
        try:
            print(temp[0])
        except IndexError:
            print("ID不存在,没有找到对应的接口信息")
            return jsonify({"msg":"ID不存在,没有找到对应的接口信息","code":400,"data":""})
        return json.dumps({"msg":"ok","code":200,"data":temp[0]})

@app.route('/help')
def testhelp():
    return render_template('help.html')

#上传文件解析处理不同编码
@app.route('/encodefile', methods=['POST'])
def encode_file():
    f = request.files['myf']
    ftype = request.form['type']
    if f and allowed_file(f.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(filepath)
        if ftype == "base64":
            with open(filepath,"rb") as tmpf:
                myencode = base64.b64encode(tmpf.read())
                myencode = "data:image/jpeg;base64," + myencode.decode()
                return myencode
        elif ftype == "binary":
            with open(filepath,"rb") as tmpf:
                myencode = tmpf.read()
                hexstr = binascii.b2a_hex(myencode) #得到一个16进制的数
                bsstr = bin(int(hexstr,16))[2:]
                print(bsstr)
                return bsstr
        elif ftype == "filestr":
            with open(filepath,"rb") as tmpf:
                myencode = tmpf.read()
                myencode = myencode.decode('utf-8')
                print(myencode)
                return myencode
        else:
            return render_template('error.html', result=())
    else:
        return render_template('error.html', result=())

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/uiauto', methods=['GET','POST'])
def uiauto():
    return render_template('uiauto.html', result=())

@app.route('/uiauto_redirect_w', methods=['GET','POST'])
def uiauto_redirect():
    get_mode = request.form["m"]
    print(get_mode)
    sk = socket.socket()
    address = (config.runui_ip2,config.runui_port)
    print(config.runui_ip)
    try:
        sk.connect(address)
    except ConnectionRefusedError:
        print('无法链接UI自动化服务器' + str(address))
   # while True:
   # inp = input('>>>>>.')
   # if inp == 'exit':
   #     break
    if get_mode == "tpa":
        inp = config.exeshell
    else:
        inp = config.exeshell
    sk.send(bytes(inp,'utf8'))
    sk.close()
    return redirect('uiauto_www')

@app.route('/uiauto_redirect_c', methods=['GET','POST'])
def uiauto_redirect_c():
    get_mode = request.form["m"]
    print(get_mode)
    sk = socket.socket()
    address = (config.runui_ip2,config.runui_port)
    print(config.runui_ip)
    sk.connect(address)
    if get_mode == "dev":
        inp = "ui_console.py dev"
    else:
        inp = "ui_console.py test"
    sk.send(bytes(inp,'utf8'))
    sk.close()
    return redirect('uiauto_www')

@app.route('/uiauto_redirect_a', methods=['GET','POST'])
def uiauto_redirect_a():
    get_mode = request.form["m"]
    print(get_mode)
    sk = socket.socket()
    address = (config.runui_ip2,config.runui_port)
    print(config.runui_ip)
    sk.connect(address)
    if get_mode == "dev":
        inp = "ui_admin.py dev"
    else:
        inp = "ui_admin.py test"
    sk.send(bytes(inp,'utf8'))
    sk.close()
    return redirect('uiauto_www')

@app.route('/uiauto_www', methods=['GET','POST'])
def uiauto_www():
    if request.method == "GET":
        try:
            get_mode = request.args.get("imode")
        except:
            get_mode = "tpa"
        if not get_mode:
            get_mode = "tpa"
        print(get_mode)
    mydata = lhlSql()
    www_result = mydata.getUiautoResult(get_mode)
    print(www_result)
    if get_mode == "task":
        logurl = "./log/casjc.log"
    else:
        logurl = config.runui_ip
    return render_template('ciics_ui_result.html', result=(www_result,logurl, random.random()))

@app.route('/jianmei', methods=['GET','POST'])
def jianmei():
    request.environ["Access-Control-Allow-Origin"] = "*"
    return render_template('jianmei.html')

@app.route('/mytestabc', methods=['GET','POST'])
def myabc():
    if request.method == "POST":
        aa = request.form
        print(aa)
        return aa,200
    else:
        print(request.values.get('a'))
        print('xxxx')
    return "OK",200

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True,port="8888")
