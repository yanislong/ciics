import pycurl
import sys 
import json
from io import BytesIO

WEB_SITES = "http://192.168.15.21:7777/login"#sys.argv[1]

def main():
    c = pycurl.Curl()
    c.setopt(pycurl.URL, WEB_SITES)              #set url
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    buffer = BytesIO()
    c.setopt(c.WRITEDATA,buffer)
    content = c.perform()                        #execute 
    dns_time = c.getinfo(pycurl.NAMELOOKUP_TIME) #DNS time
    conn_time = c.getinfo(pycurl.CONNECT_TIME)   #TCP/IP 3-way handshaking time
    starttransfer_time = c.getinfo(pycurl.STARTTRANSFER_TIME)  #time-to-first-byte time
    total_time = c.getinfo(pycurl.TOTAL_TIME)  #last requst time
    c.close()

    data = json.dumps({'dns_time':dns_time,         
                       'conn_time':conn_time,        
                       'starttransfer_time':starttransfer_time,    
                       'total_time':total_time})
    return data

if __name__ == "__main__":    
    print(main())
pycurl.error: (23, 'Failed writing body (7 != 11274)')
