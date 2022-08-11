
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



if __name__ == "__main__":
    pass
    # test_gerber_to_odb_ep()
    # vs_ep_1()
    mysql()

