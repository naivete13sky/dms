from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Org
# Create your views here.
import os
from django.http import StreamingHttpResponse
import pandas as pd
import psycopg2

def readFile(filename,chunk_size=512):
    with open(filename,'rb') as f:
        while True:
            c=f.read(chunk_size)
            if c:
                yield c
            else:
                break

def file_download_org(request,order):
    # do something
    print(request.path_info)
    print("*"*30,order)
    excel_name = str(request.path_info).replace("/router_job_org/","")
    print(excel_name)
    pwd = os.getcwd()
    the_file_name = excel_name
    filename = pwd + r"\router_job_org\\" + excel_name
    # filename=request.path_info
    print(filename)
    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response

def post_detail(request, order):
    order = get_object_or_404(Org, slug=order)
    print(order)
    # return render(request, 'blog/post/detail.html', {'order': order,})


def file_download_job_pre(request,order):
    # do something
    print(request.path_info)
    print("*"*30,order)
    excel_name = str(request.path_info).replace("/router_job_pre/","")
    print(excel_name)
    pwd = os.getcwd()
    the_file_name = excel_name
    filename = pwd + r"\router_job_pre\\" + excel_name
    print(filename)
    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response

def file_download_job_robot(request,order):
    # do something
    excel_name = str(request.path_info).replace("/router_job_robot/","")
    pwd = os.getcwd()
    the_file_name = excel_name
    filename = pwd + r"\router_job_robot\\" + excel_name
    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response

def file_download_job_feedback(request,order):
    # do something
    excel_name = str(request.path_info).replace("/router_job_feedback/","")
    pwd = os.getcwd()
    the_file_name = excel_name
    filename = pwd + r"\router_job_feedback\\" + excel_name
    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response

def file_download_job_recipe(request,order):
    # do something
    excel_name = str(request.path_info).replace("/router_job_recipe/","")
    pwd = os.getcwd()
    the_file_name = excel_name
    filename = pwd + r"\router_job_recipe\\" + excel_name
    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response

def list_all_job(request):

    # 创建连接对象
    conn = psycopg2.connect(database="ep", user="postgres", password="cc", host="10.97.80.118", port="5432")
    cursor = conn.cursor()  # 创建指针对象
    # sql="SELECT * from job_manage_pre;"
    sql="""
    SELECT a.id ID,a.company_name 公司名称,a.receive_date 接受时间,a.job_name_org 原始料号名,b.username 原始料号导入人,a.recipe_status 是否提供参数,
d.username 前处理负责人,c.pre_status 是否完成前处理,
f.username 机器人处理负责人,e.robot_status 是否完成机器人处理,
g.feedback_date 反馈时间,
h.backup_status 是否完成备份
from job_manage_org a
LEFT JOIN auth_user b on a.receive_staff_id = b.id
LEFT JOIN job_manage_pre c on a.id=c.job_name_org_id
LEFT JOIN auth_user d on c.pre_staff_id = d.id
LEFT JOIN job_manage_robot e on c.id=e.job_name_pre_id
LEFT JOIN auth_user f on e.robot_staff_id = f.id
LEFT JOIN job_manage_feedback g on a.id=g.job_name_org_id
LEFT JOIN job_manage_information h on a.id=h.job_name_org_id;
    """

    df = pd.read_sql(sql, conn)
    # print(df.columns.values.tolist())#得到列名
    table_title = df.columns.values.tolist()
    table_content = df.itertuples(index=False)
    theads = ['反馈类型', '当前状态', '数量', '时间']
    return render(request, 'list_all_job.html',{"theads": table_title, "trows": table_content})