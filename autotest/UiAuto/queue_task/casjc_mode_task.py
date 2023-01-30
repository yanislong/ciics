import re, time

import requests
from bs4 import BeautifulSoup
import pymysql
import casjc_log_task


#脚本执行结果插入到数据库
def Run_result(*resdic):
    tt = time.strftime("%Y/%m/%d %H:%M:%S")
    con = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="Casjc@20210226", database='portaltest', charset="utf8mb4")
    cursor = con.cursor()
    sql = "insert into uitestresult(mode,stime,etime,result,exectime,env) value('{0}','{1}','{2}','{3}','{4}','{5}')".format(resdic[0][0],resdic[0][1],resdic[0][2],pymysql.escape_string(resdic[0][3]),tt,resdic[0][4])
    cursor.execute(sql)
    con.commit()
    casjc_log_task.logging.info("执行结果插入到数据库")
    cursor.close()
    con.close()
    return None

if __name__ == "__main__":
    pass
