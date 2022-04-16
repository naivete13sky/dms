from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404,HttpResponse
from .models import Job
# Create your views here.
import os
from django.http import StreamingHttpResponse
import pandas as pd
import psycopg2
from pathlib import Path
from django.conf import settings
from job_manage.forms import UserForm
from job_manage import models


def readFile(filename,chunk_size=512):
    with open(filename,'rb') as f:
        while True:
            c=f.read(chunk_size)
            if c:
                yield c
            else:
                break

def file_download_odb(request,order):
    # do something
    print(request.path_info)
    print("*"*30,order)
    excel_name = str(request.path_info).replace("/router_job_odb/","")
    print(excel_name)
    pwd = os.getcwd()
    the_file_name = excel_name
    filename = pwd + r"\router_job_odb\\" + excel_name
    # filename=request.path_info
    print(filename)
    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response

def post_detail(request, order):
    order = get_object_or_404(Job, slug=order)
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

def job_upload(request):
    return render(request,r'../templates/job_upload.html')

# ajax上传文件
def job_upload_ajax(request):
    if request.method=='GET':
        return render(request,r'../templates/upload.html')
    elif request.method=='POST':

        # psd = request.POST.get('password')
        file_odb = request.FILES.get('file_odb')
        file_odb_name = file_odb.name
        # 拼接绝对路径
        file_odb_path = os.path.join(settings.BASE_DIR, 'upload', file_odb_name)
        with open(file_odb_path, 'wb')as f:
            for chunk in file_odb.chunks():#chunks()每次读取数据默认我64k
                f.write(chunk)
        #压缩文件
        file_compressed = request.FILES.get('file_compressed')
        file_compressed_name = file_compressed.name
        # print(file_compressed_name)
        # 拼接绝对路径
        file_compressed_path = os.path.join(settings.BASE_DIR, 'upload', file_compressed_name)
        with open(file_compressed_path, 'wb')as f:
            for chunk in file_compressed.chunks():  # chunks()每次读取数据默认我64k
                f.write(chunk)
        job_name = request.POST.get('job_name')
        print(job_name)
        return HttpResponse('完成上传')

def reg(request):
  form = UserForm()
  if request.method == "POST":
    # print(request.POST)
    # 实例化form对象的时候，把post提交过来的数据直接传进去
    form = UserForm(request.POST) # form表单的name属性值应该与forms组件的字段名称一致
    if form.is_valid():
      print(form.cleaned_data)
      return HttpResponse('注册成功')
  return render(request, r'../templates/reg.html', locals())