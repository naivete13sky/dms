import subprocess
import time

import psycopg2
import rarfile
import os,sys
sys.path.append(r'C:\cc\python\epwork\dms\job_manage\g')
from django.conf import settings
import psycopg2
import os,sys,json,shutil
path = os.path.dirname(os.path.realpath(__file__)) + r'/epcam'
from django.conf import settings
print(path)
sys.path.append(path)
import epcam
import epcam_api
import job_operation


def mysql():
    pass
    import pandas as pd
    from sqlalchemy import create_engine
    import time
    engine = create_engine("mysql+mysqlconnector://chencheng:hWx9pWk5d5J@10.97.80.36:3336/zentao")
    # conn= pymysql.connect(host="10.97.80.36",user="chencheng",passwd="hWx9pWk5d5J",port=3336,db="zentao")
    sql = '''SELECT a.*,b.name productname,c.realname createbywho,d.realname assignedtowho from zt_bug a
    LEFT JOIN zt_product b on a.product=b.id
    LEFT JOIN zt_user c on a.openedBy=c.account
    LEFT JOIN zt_user d on a.assignedTo=d.account
    where a.deleted='0'
    '''
    # bug_pd=pd.read_sql(sql=sql,con=conn)
    bug_pd = pd.read_sql_query(sql, engine)
    # bug_pd.to_excel(r"c:\report\data\temp\EP-CAM-Bug.xlsx",index=False)
    # bug_pd.to_excel(r"c:\report\data\temp\EP-CAM-Bug-%s.xlsx"%(time.time()),index=False)

    bug_pd_sta_by_opened_date = bug_pd.groupby(['pri'])['id'].count()
    # print(bug_pd_sta_by_opened_date)

    sql = '''SELECT a.* from zt_bug a
    where a.id=1260
            '''
    bug_pd = pd.read_sql_query(sql, engine)
    print(bug_pd['title'][0])



def mysql2():
    pass
    import pandas as pd
    from sqlalchemy import create_engine
    import time
    engine = create_engine("mysql+mysqlconnector://chencheng:hWx9pWk5d5J@10.97.80.36:3336/zentao")
    # conn= pymysql.connect(host="10.97.80.36",user="chencheng",passwd="hWx9pWk5d5J",port=3336,db="zentao")
    sql = '''SELECT a.*,b.name productname,c.realname createbywho,d.realname assignedtowho from zt_bug a
    LEFT JOIN zt_product b on a.product=b.id
    LEFT JOIN zt_user c on a.openedBy=c.account
    LEFT JOIN zt_user d on a.assignedTo=d.account
    where a.deleted='0'
    '''

    with engine.connect() as con:
        pass
        sql = '''SELECT a.* from zt_bug a
    where a.id=1264
            '''
        result=con.execute(sql)
        print(result)
        for each in result:
            print(each)

def pg():
    pass
    conn = psycopg2.connect(database="dms", user="readonly", password="123456", host="10.97.80.147", port="5432")
    cursor = conn.cursor()
    sql='''SELECT * from job a
where a.id=2
    '''
    cursor.execute(sql)
    conn.commit()
    ans = cursor.fetchall()
    conn.close()
    return ans

import tarfile as tf
def maketgz(ifn, out_path, file_name):
    """压缩文件夹为tgz
    :param     ifn(str):导入路径
    :param     out_path(str):导出路径
    :param     file_name(str):文件名
    :returns   :None
    :raises    error:
    """
    try:
        ifn = ifn.split(sep = '"')[1]
    except:
        pass
    file_real_name = file_name.split('.')[0]
    ofn = out_path + '\\' + file_name #+ '.tgz'
    #最外层后缀也为tar, 然后再rename为tgz
    out_ofn = out_path + '\\' + file_real_name + '.tar'
    #with tf.open(ofn, 'w:gz') as tar:
    with tf.open(out_ofn, 'w:gz') as tar:
        tar.add(ifn, arcname = os.path.basename(ifn))
    if os.path.exists(ofn):
        os.remove(ofn)
    os.rename(out_ofn, ofn)
    print('compress success!')
        #os.system('pause')

    return 0

import functools
def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            print("函数内部参数:",*args,*kw)
            print("函数内部参数,第2个:",args[1])
            return func(*args, **kw)
        return wrapper
    return decorator

@log("abc")
def now(p1,p2):
    print('2015-3-25')
    print("p1",p1,"p2",p2)



def g_current_odb_view(job_path,job):
    pass

    #show epcam



    # 删除temp_path
    # if os.path.exists(job_path):
    #     shutil.rmtree(job_path)

def job_create_test():
    pass
    epcam.init()
    epcam_api.create_job(r"C:\cc\share", "abc")
    epcam_api.open_job(r"C:\cc\share", "abc")
    epcam_api.close_job("abc")

    time.sleep(5)
    epcam_api.delete_job("abc")
    time.sleep(5)

    epcam_api.create_job(r"C:\cc\share", "ccc")
    epcam_api.close_job("ccc")
    epcam_api.create_job(r"C:\cc\share", "abc")


def job_create_test2():
    pass
    epcam.init()
    epcam_api.create_job(r"C:\cc\share", "abc")
    epcam_api.open_job(r"C:\cc\share", "abc")
    epcam_api.close_job("abc")

    # time.sleep(5)
    epcam_api.close_job("abc")
    # epcam_api.delete_job("abc")
    print("close job")
    time.sleep(10)

    epcam_api.create_job(r"C:\cc\share", "ccc")
    epcam_api.close_job("ccc")
    epcam_api.create_job(r"C:\cc\share", "abc")

import functools

strs = [3, 4, 1, 2]


# 自定义排序规则
def my_compare(x, y):
    if x > y:
        return 1
    elif x < y:
        return -1
    return 0

def list_sort_test():
    pass
    import functools
    strs = [3, 4, 1, 2]
    # 分别使用sorted和list.sort
    print(strs)
    print(sorted(strs, key=functools.cmp_to_key(my_compare)))
    print(strs)
    strs.sort(key=functools.cmp_to_key(my_compare))
    print(strs)


if __name__ == "__main__":
    pass
    # test_gerber_to_odb_ep()
    # vs_ep_1()
    # mysql()
    # print(pg())
    # maketgz(r'C:\cc\share\temp_cc_9\01234567890123456789012',r'C:\cc\share\temp_cc_9',r'01234567890123456789012.tgz')

    # now(1,2)
    job_create_test2()
    # list_sort_test




