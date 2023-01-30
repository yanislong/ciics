import socket
import subprocess
#cmd模块
#subprocess.Popen()
sk = socket.socket()
address = ('0.0.0.0',8000)
sk.bind(address)
sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
sk.listen(3)

print('writing..........')
while True:
    conn,addr = sk.accept()
    print(addr)
    while True:
        try:
            data = conn.recv(1024)
        except Exception:
            break
        print(str(data,'utf8'))
        #拿到一个对象
        obj = subprocess.Popen(str(data,'gbk'),shell=True,stdout=subprocess.PIPE)
        cmd_result = obj.stdout.read()
        #int类型和bytes类型不能直接转换，需要中间人str，才能进行转换
        #result_len = bytes(str(len(cmd_result)),'utf8')
        #conn.sendall(result_len)
        #conn.sendall(cmd_result)
        print(str(cmd_result,'gbk'))
        if not data:break
        # inp = input('>>>>>>>>')
        # conn.send(bytes(inp,'utf8'))
conn.close()
sk.close()
