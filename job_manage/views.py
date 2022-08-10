# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from django.shortcuts import render, get_object_or_404,HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.http import StreamingHttpResponse
from django.shortcuts import render,redirect,HttpResponse
from django.conf import settings
import pandas as pd
import psycopg2
import time
import rarfile
from pathlib import Path
from django.db.models import Q
from dms.settings import MEDIA_URL
from job_manage.forms import UserForm,UploadForms,ViewForms,UploadForms_no_file,JobFormsReadOnly,ShareForm
from job_manage import models
from django.contrib.sites.models import Site
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from taggit.models import Tag

from os.path import dirname, abspath
import os,sys,json,shutil
path = os.path.dirname(os.path.realpath(__file__)) + r'/epcam'
sys.path.append(path)
import epcam
import epcam_api
from cc_method import Tgz

import re
base_path = dirname(dirname(abspath(__file__)))
sys.path.insert(0, base_path)
# print("*"*100)
# print("bathpath",base_path)
# print(sys.path)
# print("*"*100)
path_epcam_cc_method=os.path.join(base_path,r'job_manage')
sys.path.append(path_epcam_cc_method)
import job_operation
import layer_info
from epcam_cc_method import EpGerberToODB
import gl as gl
from g_cc_method import Asw
from django.conf import settings
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dms.settings")
from .forms import LayerFormsReadOnly

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
    # pwd = os.getcwd()
    pwd=settings.PROJECT_PATH

    the_file_name = excel_name
    filename = pwd + r"\router_job_odb\\" + excel_name
    # filename=request.path_info
    print(filename)
    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response

def file_download(request,order):
    # do something
    print(request.path_info)
    print("*"*30,order)
    excel_name = str(request.path_info).replace("/media/files/","")
    print(excel_name)
    # pwd = os.getcwd()
    pwd=settings.PROJECT_PATH
    the_file_name = excel_name
    filename = pwd + r"\media\files\\" + excel_name
    # filename=request.path_info
    print(filename)
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
        return render(request,r'../templates/job_upload.html')
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
        remark = request.POST.get('remark')
        author = request.POST.get('author')
        print("*"*30,job_name)

        job = Job(file_odb=file_odb, file_compressed=file_compressed,
                  job_name=job_name, remark=remark, author=author)
        job.save()

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

def Edit(request,id):
    job = models.Job.objects.filter(id=id).first()
    # print(job)
    #获取修改数据的表单
    if request.method == "GET":
        form = UploadForms(instance=job)
        return render(request, r'../templates/edit.html', locals())
    #POST请求添加修改过后的数据
    form = UploadForms(data=request.POST,instance=job)
    # print(form)
    #对数据验证并且保存
    if form.is_valid():
        print("valid")
        file_odb = request.FILES.get('file_odb')
        if file_odb != None:
            print(file_odb)
            job.file_odb = file_odb
        file_compressed = request.FILES.get('file_compressed')
        if file_compressed != None:
            print(file_compressed)
            job.file_compressed = file_compressed
        form.save()
    # return HttpResponse('数据修改成功！！')
    status = "修改成功！"
    return render(request, r'../templates/edit.html', {"status": status})

# 导入表单验证
from .forms import AddForms
class AddArticle(View):
    def get(self, request):
        return render(request, r'../templates/ModelFormTest/add.html')

    def post(self, request):
        form = AddForms(request.POST)
        # is_valid:代表验证通过的情况下
        if form.is_valid():
            # print(form)
            form.save()  # 保存完之后在数据库中显示正常
            return HttpResponse('success')
        else:
            print(form.errors.get_json_data())
            return HttpResponse('fail')

from .forms import RegisterForm
class RegisterArticle(View):
    def get(self, request):
        return render(request, r'../templates/ModelFormTest/register.html')

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.password = form.cleaned_data.get('pwd1')
            user.save()
            return HttpResponse('注册成功')
        else:
            print(form.errors.get_json_data())
            return HttpResponse('fail')

from .forms import Job
class UploadFiles(View):
    def get(self, request):
        return render(request, r'../templates/ModelFormTest/upload.html')

    def post(self, request):
        # # print(request.POST)
        # # 当选择文件上传的时候,应该选择的是FILES该文件
        # print(request.FILES)  # <MultiValueDict: {'images': [<InMemoryUploadedFile: thumb-1920-771788.png (image/png)>]}>
        # images = request.FILES.get('images')
        # print(images)  # thumb-1920-771788.png 打印的是图片的名字
        # print(type(images))  # 但是这张图片是一个类
        # with open('demo.png', 'wb')as f:
        #     f.write(images.read())
        # return HttpResponse('success')
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.POST.get('author')
        create_time = request.POST.get('create_time')
        # 当接收文件的时候使用的是FILES这个文件方式来进行接收
        images = request.FILES.get('images')
        print("*"*20,images)
        article = Job(title=title, content=content, author=author, images=images)
        article.save()
        return HttpResponse('success')

class JobUpload(View):
    def get(self, request):
        # return render(request, r'../templates/joblist.html')
        return render(request, r'../templates/upload.html')

    def post(self, request):
        file_odb = request.FILES.get('file_odb')
        file_compressed = request.FILES.get('file_compressed')
        job_name = request.POST.get('job_name')
        remark = request.POST.get('remark')
        slug = request.POST.get('slug')
        author = request.POST.get('author')
        create_time = request.POST.get('create_time')
        job = Job(file_odb=file_odb, file_compressed=file_compressed,
                  job_name=job_name, remark=remark,slug=slug,
                  author=author)
        job.save()
        # return HttpResponse('success')
        status="上传成功！"
        return render(request, r'../templates/upload.html',{"status":status})

# @login_required#可以url中加装饰器
def job_view(request,tag_slug=None):
    if request.method == "POST":
        pass
        # print("post")
        query=request.POST.get('query')
        if query:
            # print(request.POST.get('query'))
            job_list = models.Job.objects.all().filter(Q(job_name__contains=query)
                                                       |Q(author__username__contains=query)
                                                       # |Q(tags__exact=query)
                                                       )
        else:
            query=''
            job_list = models.Job.objects.all()
    else:
        job_list = models.Job.objects.all()
    # job_list = models.Job.objects.all().order_by('-publish')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        job_list = models.Job.objects.filter(tags__in=[tag])

    job_field_verbose_name=[Job._meta.get_field('job_name').verbose_name,
                            Job._meta.get_field('file_odb').verbose_name,
                            Job._meta.get_field('file_compressed').verbose_name,
                            Job._meta.get_field('remark').verbose_name,
                            Job._meta.get_field('author').verbose_name,
                            Job._meta.get_field('publish').verbose_name,
                            "操作",
                            ]

    #附件超链接
    current_site = Site.objects.get_current()
    # print(current_site,"***",MEDIA_URL)
    # print(current_site)
    return render(request, r'../templates/view.html',
                  {'job_list': job_list,
                   'job_field_verbose_name':job_field_verbose_name,
                   'current_site':current_site,
                   'tag': tag
                   })

def add(request):
    if request.method == "GET":
        form = UploadForms_no_file()
        return render(request, "add.html", {"form": form})
    else:
        form = UploadForms_no_file(request.POST)
        if form.is_valid():  # 进行数据校验
            # 校验成功
            data = form.cleaned_data  # 校验成功的值，会放在cleaned_data里。
            # data.pop('job_name')
            print(data)
            file_odb = request.FILES.get('file_odb')
            file_compressed = request.FILES.get('file_compressed')
            data["file_odb"]=file_odb
            data["file_compressed"] = file_compressed

            models.Job.objects.create(**data)
            # return HttpResponse('ok' )
            up_status="新增完成！"
            return render(request, "add.html", {"form": form,"up_status":up_status})
        else:
            print(form.errors)    # 打印错误信息
            clean_errors = form.errors.get("__all__")
            print(222, clean_errors)
        return render(request, "add.html", {"form": form, "clean_errors": clean_errors})

def job_list(request,tag_slug=None):
    object_list = Job.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = models.Job.objects.filter(tags__in=[tag])
    # object_list = Job.published.all()
    paginator = Paginator(object_list, 5)  # 每页显示5篇文章
    page = request.GET.get('page')
    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        # 如果page参数不是一个整数就返回第一页
        jobs = paginator.page(1)
    except EmptyPage:
        # 如果页数超出总页数就返回最后一页
        jobs = paginator.page(paginator.num_pages)

    # return render(request, 'blog/post/list.html', {'posts': posts})
    return render(request, 'list.html', {'page': page, 'jobs': jobs,'tag': tag})


class JobListViewVs(ListView):
    queryset = models.Job.objects.all()
    # model=models.Job
    context_object_name = 'jobs'
    paginate_by = 10
    # ordering = ['-publish']
    template_name = 'JobListView.html'

    # def get_queryset(self):
    #     query = self.request.GET.get('query', '')
    #     new_context = models.Job.objects.filter(
    #             Q(job_name__contains=query) |
    #             Q(author__username__contains=query))
    #     return new_context
    # def get_queryset(self):  # 重写get_queryset方法
    #     # 获取所有is_deleted为False的用户，并且以时间倒序返回数据
    #     return UserProfile.objects.filter(is_deleted=False).order_by('-create_time')

    def get_context_data(self, **kwargs):  # 重写get_context_data方法
        # 很关键，必须把原方法的结果拿到
        context = super().get_context_data(**kwargs)
        job_field_verbose_name = [Job._meta.get_field('job_name').verbose_name,
                                  Job._meta.get_field('file_odb').verbose_name,
                                  Job._meta.get_field('file_compressed').verbose_name,
                                  Job._meta.get_field('file_compressed_org').verbose_name,
                                  Job._meta.get_field('remark').verbose_name,
                                  Job._meta.get_field('author').verbose_name,
                                  Job._meta.get_field('from_object').verbose_name,
                                  # Job._meta.get_field('publish').verbose_name,
                                  Job._meta.get_field('create_time').verbose_name,
                                  Job._meta.get_field('updated').verbose_name,
                                  "标签",
                                  "操作",
                                  ]
        context['job_field_verbose_name'] = job_field_verbose_name# 表头用
        query=self.request.GET.get('query',False)
        if query:
            # context['cc'] = query
            # print(query)
            # context['query'] = query
            context['jobs'] = models.Job.objects.filter(
                Q(job_name__contains=query) |
                Q(from_object__contains=query) |
                Q(author__username__contains=query))
        return context

class JobListView(ListView):
    queryset = models.Job.objects.all()
    # model=models.Job
    context_object_name = 'jobs'
    paginate_by = 10
    # ordering = ['-publish']
    template_name = 'JobListView.html'

    def get_context_data(self, **kwargs):  # 重写get_context_data方法
        # 很关键，必须把原方法的结果拿到
        context = super().get_context_data(**kwargs)
        job_field_verbose_name = [Job._meta.get_field('job_name').verbose_name,
                                  Job._meta.get_field('file_compressed').verbose_name,
                                  Job._meta.get_field('file_compressed_org').verbose_name,
                                  Job._meta.get_field('file_odb').verbose_name,
                                  Job._meta.get_field('file_odb_current').verbose_name,
                                  Job._meta.get_field('file_odb_g').verbose_name,
                                  Job._meta.get_field('vs_result_ep').verbose_name,
                                  Job._meta.get_field('vs_result_g').verbose_name,
                                  '层别信息',
                                  Job._meta.get_field('remark').verbose_name,
                                  Job._meta.get_field('author').verbose_name,
                                  Job._meta.get_field('from_object').verbose_name,
                                  # Job._meta.get_field('publish').verbose_name,
                                  Job._meta.get_field('create_time').verbose_name,
                                  Job._meta.get_field('updated').verbose_name,
                                  "标签",
                                  "操作",
                                  ]
        context['job_field_verbose_name'] = job_field_verbose_name# 表头用



        query=self.request.GET.get('query',False)
        if query:
            # context['cc'] = query
            # print(query)
            # context['query'] = query
            context['jobs'] = models.Job.objects.filter(
                Q(job_name__contains=query) |
                Q(from_object__contains=query) |
                Q(author__username__contains=query))
        return context

class JobDetailView(DetailView):
    model = Job
    template_name = "detail_listview.html"
    context_object_name = "job"
    pk_url_kwarg = "pk"  # pk_url_kwarg默认值就是pk，这里可以覆盖，但必须和url中的命名组参数名称一致
    def get(self, request, *args, **kwargs):
        # print('get url parms: ' + kwargs['pk'])
        job = models.Job.objects.filter(id=kwargs['pk']).first()
        form = JobFormsReadOnly(instance=job)
        return self.render_to_response({'form': form})

class JobFormView(FormView):
    form_class = JobFormsReadOnly
    template_name = "detail_listview.html"

    def get(self, request, *args, **kwargs):
        # print('get url parms: ' + kwargs['parm'])
        job = models.Job.objects.filter(id=kwargs['parm']).first()
        form = self.form_class(instance=job)
        return self.render_to_response({'form': form})

def job_detail(request, year, month, day, job):
    job = get_object_or_404(Job, slug=job, status="published", publish__year=year, publish__month=month,
                             publish__day=day)
    form=JobFormsReadOnly(instance=job)
    return render(request, r'../templates/detail.html', {'job': job,'form':form})

def del_job(request, job_id):
    # job = Job.objects.get(id=job_id)
    # return render(request, 'del_job.html', {'job': job})
    job = models.Job.objects.filter(id=job_id).first()
    # print(job)
    # 获取修改数据的表单
    if request.method == "GET":
        form = UploadForms(instance=job)
        return render(request, r'../templates/del_job.html', locals())
    if request.method == 'POST':
        job.delete()
        return redirect('job_manage:job_view')

def share_job(request, job_id):
    job = models.Job.objects.filter(id=job_id).first()
    # print(job)
    # print(job.id)
    # print(job.job_name)
    # share_account = models.ShareAccount.objects.all()
    share_account = models.ShareAccount.objects.filter(share_job=job_id)
    # print(share_account)
    # for each in share_account:
    #     print(each)
    # print(share_account[0])
    field_verbose_name=['用户','备注']

    # 获取修改数据的表单
    if request.method == "GET":
        # form = JobFormsReadOnly(instance=job)
        # for each in share_account:
        #     form_share=ShareForm(instance=each)

        form=ShareForm()
        return render(request, r'../templates/share_job.html',
                      {
                        "form":form,
                       "share_account":share_account,
                       'field_verbose_name':field_verbose_name,
                       'job_name':job.job_name}

        )
    if request.method == 'POST':
        pass
        form = ShareForm(request.POST)
        if form.is_valid():  # 进行数据校验
            # 校验成功
            data = form.cleaned_data  # 校验成功的值，会放在cleaned_data里。
            data["share_job"]=job
            print(data)
            models.ShareAccount.objects.create(**data)
            up_status = "新增完成！"
            # return render(request, "share_job.html", {"form": form, "up_status": up_status})
            return render(request, r'../templates/share_job.html',
                          {
                              "form": form,
                              "share_account": share_account,
                              'field_verbose_name': field_verbose_name,
                              'job_name': job.job_name,
                              "up_status": up_status
                          }

                          )
        else:
            print(form.errors)  # 打印错误信息
            clean_errors = form.errors.get("__all__")
            print(222, clean_errors)
        return render(request, "share_job.html", {"form": form, "clean_errors": clean_errors})

def job_analysis(request):
    pass
    return render(request, r'job_analysis.html', locals())

#这种方式上传附件是可以的
class JobCreateView(CreateView):
    model=Job
    template_name = "JobCreateView.html"
    fields = "__all__"

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(JobCreateView, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['author'] = self.request.user
        # etc...
        return initial

    success_url = 'JobListView'

class JobUpdateView(UpdateView):
    """
    该类必须要有一个pk或者slug来查询（会调用self.object = self.get_object()）
    """
    model = Job
    fields = "__all__"
    # template_name_suffix = '_update_form'  # html文件后缀
    template_name = 'JobUpdateView.html'
    success_url = '../JobListView' # 修改成功后跳转的链接

class JobUpdateViewVs(UpdateView):
    """
    该类必须要有一个pk或者slug来查询（会调用self.object = self.get_object()）
    """
    model = Job
    fields = "__all__"
    # template_name_suffix = '_update_form'  # html文件后缀
    template_name = 'JobUpdateView.html'
    success_url = '../JobListView' # 修改成功后跳转的链接

class JobDeleteView(DeleteView):
  """
  """
  model = Job
  template_name = 'JobDeleteView.html'
  # template_name_field = ''
  # template_name_suffix = ''
  # book_delete.html为models.py中__str__的返回值
   # namespace:url_name
  success_url = reverse_lazy('job_manage:job_view')


def job_settings(request):
    pass
    return render(request, r'job_settings.html', locals())

def get_file_name_from_org(request,job_id):
    pass
    print(job_id)
    # 找到job对象
    job = Job.objects.get(id=job_id)
    #先删除原来已有的层信息
    layer_old=models.Layer.objects.filter(job=job)
    print(layer_old)
    layer_old.delete()


    print(job.job_name, job.file_compressed)

    # 先拿到原始料号，放到临时文件夹，完成解压
    temp_path = r'C:\cc\share\temp'+"_"+str(request.user)+"_"+str(job_id)
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)
    # org_file_path = (os.path.join(os.getcwd(), r'media', str(job.file_compressed))).replace(r'/', '\\')
    org_file_path = (os.path.join(settings.PROJECT_PATH, r'media', str(job.file_compressed))).replace(r'/', '\\')
    shutil.copy(org_file_path, temp_path)
    time.sleep(0.2)
    rf = rarfile.RarFile(os.path.join(temp_path, str(job.file_compressed).split("/")[1]))
    rf.extractall(temp_path)
    temp_compressed = os.path.join(temp_path, str(job.file_compressed).split("/")[1])
    if os.path.exists(temp_compressed):
        os.remove(temp_compressed)
    file_path_gerber = os.listdir(temp_path)[0]
    print(file_path_gerber)
    # for root, dirs, files in os.walk(os.path.join(temp_path,file_path_gerber)):
    #     for file in files:
    #         if EpGerberToODB().is_chinese(file):
    #             print("*"*30,str(os.path.join(temp_path,file_path_gerber)) + r'/' + file)
    #             os.rename(str(os.path.join(temp_path,file_path_gerber)) + r'/' + file, str(os.path.join(temp_path,file_path_gerber)) + r'/''unknow' + str(index))
    #             file = 'unknow' + str(index)
    #             index = index + 1
    #         print(file)


    list = os.listdir(os.path.join(temp_path,file_path_gerber))  # 列出文件夹下所有的目录与文件
    index=1
    for i in range(0, len(list)):
        path = os.path.join(os.path.join(temp_path,file_path_gerber), list[i])
        if os.path.isfile(path):
            pass
            print(path)
            file_name=list[i]
            file_name_org=list[i]
            if EpGerberToODB().is_chinese(path):
                pass
                os.rename(path,os.path.join(temp_path,file_path_gerber,'unknow' + str(index)))
                file_name='unknow' + str(index)
                index=index+1
            file_name=file_name.replace(' ','-')
            layer_new = models.Layer()
            layer_new.job=job
            layer_new.layer=file_name
            layer_new.layer_org=file_name_org
            layer_new.save()
    # 删除temp_path
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)

    job.bool_layer_info='true'
    job.save()
    # return redirect('job_manage:JobListViewVs')
    return redirect('../../view_layer/{}'.format(job_id))

def get_file_name_from_org_on(request,job_id):
    pass
    print(job_id)
    # 找到job对象
    job = Job.objects.get(id=job_id)
    # #先删除原来已有的层信息
    # layer_old=models.Layer.objects.filter(job=job)
    # print(layer_old)
    # layer_old.delete()


    print(job.job_name, job.file_compressed)

    #false时就在前端显示生成的按钮。
    job.bool_layer_info='false'
    job.save()
    # return redirect('job_manage:JobListViewVs')
    return redirect('../../JobListView')

def delete_all_layer_info(request,job_id):
    pass
    print(job_id)
    # 找到job对象
    job = Job.objects.get(id=job_id)
    #先删除原来已有的层信息
    layer_old=models.Layer.objects.filter(job=job)
    print(layer_old)
    layer_old.delete()
    print(job.job_name, job.file_compressed)
    job.bool_layer_info='false'
    job.save()
    # return redirect('job_manage:JobListViewVs')
    return redirect('../../view_layer/{}'.format(job_id))

def gerber274x_to_odb_ep(request,job_id):
    pass

    #找到job对象
    job=Job.objects.get(id=job_id)
    print(job.job_name,job.file_compressed)


    #先拿到原始料号，放到临时文件夹，完成解压
    temp_path=r'C:\cc\share\temp'+"_"+str(request.user)+"_"+str(job_id)
    print("*"*100,temp_path)
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)
    org_file_path=(os.path.join(settings.PROJECT_PATH,r'media',str(job.file_compressed))).replace(r'/','\\')
    shutil.copy(org_file_path,temp_path)
    time.sleep(0.2)
    rf = rarfile.RarFile(os.path.join(temp_path,str(job.file_compressed).split("/")[1]))
    rf.extractall(temp_path)
    temp_compressed=os.path.join(temp_path,str(job.file_compressed).split("/")[1])
    if os.path.exists(temp_compressed):
        os.remove(temp_compressed)
    #epcam 导入
    epcam.init()
    file_path_gerber = os.listdir(temp_path)[0]
    job_name = file_path_gerber + '_ep_'+str(int(time.time()))
    step = 'orig'

    # print(file_path_gerber)


    file_path = os.path.join(temp_path,file_path_gerber)
    out_path = temp_path
    cc = EpGerberToODB()
    cc.ep_gerber_to_odb(job_name, step, file_path, out_path)
    #把悦谱转图压缩成tgz。
    ifn = os.path.join(temp_path,job_name)
    try:
        ifn = ifn.split(sep='"')[1]
        # print(ifn)
    except:
        pass
    ofn = ifn + '.tgz'
    Tgz().maketgz(ofn, ifn)

    #把压缩好悦谱转图tzg放入相应Job里
    shutil.copy(os.path.join(temp_path,job_name+'.tgz'), os.path.join(settings.PROJECT_PATH,r'media\files'))
    time.sleep(0.2)

    job.file_odb_current=('files/'+job_name+'.tgz')
    job.save()
    #删除ep.tzg
    if os.path.exists(os.path.join(temp_path,job_name+'.tgz')):
        os.remove(os.path.join(temp_path,job_name+'.tgz'))
    # 删除temp_path
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)



    return redirect('job_manage:JobListView')

def gerber274x_to_odb_ep2(request,job_id):
    pass
    #gerber274x_to_odb_ep2:孔参数取自数据库，而gerber274x_to_odb_ep是根据软件默认的参数导入的

    #找到job对象
    job=Job.objects.get(id=job_id)
    print(job.job_name,job.file_compressed)


    #先拿到原始料号，放到临时文件夹，完成解压
    temp_path=r'C:\cc\share\temp'+"_"+str(request.user)+"_"+str(job_id)
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)
    org_file_path=(os.path.join(settings.PROJECT_PATH,r'media',str(job.file_compressed))).replace(r'/','\\')
    shutil.copy(org_file_path,temp_path)
    time.sleep(0.2)
    rf = rarfile.RarFile(os.path.join(temp_path,str(job.file_compressed).split("/")[1]))
    rf.extractall(temp_path)
    temp_compressed=os.path.join(temp_path,str(job.file_compressed).split("/")[1])
    if os.path.exists(temp_compressed):
        os.remove(temp_compressed)
    #epcam 导入
    epcam.init()
    file_path_gerber = os.listdir(temp_path)[0]
    job_name = file_path_gerber + '_ep_'+str(int(time.time()))
    step = 'orig'

    # print(file_path_gerber)


    file_path = os.path.join(temp_path,file_path_gerber)
    out_path = temp_path


    cc = EpGerberToODB()
    print("*"*100,job_name, step, file_path, out_path,job_id)
    cc.ep_gerber_to_odb2(job_name, step, file_path, out_path,job_id)
    #把悦谱转图压缩成tgz。
    ifn = os.path.join(temp_path,job_name)
    try:
        ifn = ifn.split(sep='"')[1]
        # print(ifn)
    except:
        pass
    ofn = ifn + '.tgz'
    Tgz().maketgz(ofn, ifn)

    #把压缩好悦谱转图tzg放入相应Job里
    shutil.copy(os.path.join(temp_path,job_name+'.tgz'), os.path.join(settings.PROJECT_PATH,r'media\files'))
    time.sleep(0.2)

    job.file_odb_current=('files/'+job_name+'.tgz')
    job.save()
    #删除ep.tzg
    if os.path.exists(os.path.join(temp_path,job_name+'.tgz')):
        os.remove(os.path.join(temp_path,job_name+'.tgz'))
    # 删除temp_path
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)



    return redirect('job_manage:JobListView')

def getFlist(path):
    for root, dirs, files in os.walk(path):
        print('root_dir:', root)  #当前路径
        print('sub_dirs:', dirs)   #子文件夹
        print('files:', files)     #文件名称，返回list类型
    return files

def gerber274x_to_odb_g(request,job_id):
    pass
    #远程调用G软件

    #找到job对象
    job=Job.objects.get(id=job_id)
    print(job.job_name,job.file_compressed)


    #先拿到原始料号，放到临时文件夹，完成解压
    temp_path=r'C:\cc\share\temp'+"_"+str(request.user)+"_"+str(job_id)
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)
    org_file_path=(os.path.join(settings.PROJECT_PATH,r'media',str(job.file_compressed))).replace(r'/','\\')
    shutil.copy(org_file_path,temp_path)
    time.sleep(0.2)
    rf = rarfile.RarFile(os.path.join(temp_path,str(job.file_compressed).split("/")[1]))
    rf.extractall(temp_path)
    temp_compressed=os.path.join(temp_path,str(job.file_compressed).split("/")[1])
    if os.path.exists(temp_compressed):
        os.remove(temp_compressed)
    #g 导入

    file_path_gerber = os.listdir(temp_path)[0]
    job_name = file_path_gerber + '_g_'+str(int(time.time()))
    step = 'orig'

    # print(file_path_gerber)


    file_path = os.path.join(temp_path,file_path_gerber)
    gerberList = getFlist(file_path)
    print(gerberList)
    g_temp_path=r'Z:/share/temp'+"_"+str(request.user)+"_"+str(job_id)
    gerberList_path = []
    for each in gerberList:
        gerberList_path.append(os.path.join(g_temp_path,file_path_gerber, each))
    print(gerberList_path)
    out_path = temp_path

    # print('gl:',settings.G_GETWAY_PATH)
    cc = Asw(settings.G_GETWAY_PATH)
    cc.g_Gerber2Odb2(job_name, step, gerberList_path, out_path,job_id)
    #输出tgz到指定目录
    cc.g_export(job_name, g_temp_path)
    #在g软件中删除此料
    cc.delete_job(job_name)

    #把g转图tzg放入相应Job里
    shutil.copy(os.path.join(temp_path,job_name+'.tgz'), os.path.join(settings.PROJECT_PATH,r'media\files'))
    time.sleep(0.2)

    job.file_odb_g=('files/'+job_name+'.tgz')
    job.save()
    #删除ep.tzg
    if os.path.exists(os.path.join(temp_path,job_name+'.tgz')):
        os.remove(os.path.join(temp_path,job_name+'.tgz'))
    # 删除temp_path
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)



    return redirect('job_manage:JobListView')


class LayerListView(ListView):
    queryset = models.Layer.objects.all()
    # model=models.Job
    context_object_name = 'layers'
    paginate_by = 10
    # ordering = ['-publish']
    template_name = 'LayerListView.html'

    # def get_queryset(self):
    #     query = self.request.GET.get('query', '')
    #     new_context = models.Job.objects.filter(
    #             Q(job_name__contains=query) |
    #             Q(author__username__contains=query))
    #     return new_context
    # def get_queryset(self):  # 重写get_queryset方法
    #     # 获取所有is_deleted为False的用户，并且以时间倒序返回数据
    #     return UserProfile.objects.filter(is_deleted=False).order_by('-create_time')

    def get_context_data(self, **kwargs):  # 重写get_context_data方法
        # 很关键，必须把原方法的结果拿到
        context = super().get_context_data(**kwargs)
        field_verbose_name = [models.Layer._meta.get_field('job').verbose_name,
                              models.Layer._meta.get_field('layer').verbose_name,
                              models.Layer._meta.get_field('layer_org').verbose_name,
                              models.Layer._meta.get_field('vs_result_manual').verbose_name,
                              models.Layer._meta.get_field('vs_result_ep').verbose_name,
                              models.Layer._meta.get_field('vs_result_g').verbose_name,
                              models.Layer._meta.get_field('layer_file_type').verbose_name,
                              models.Layer._meta.get_field('layer_type').verbose_name,
                              models.Layer._meta.get_field('features_count').verbose_name,
                              models.Layer._meta.get_field('units_ep').verbose_name,
                              models.Layer._meta.get_field('zeroes_omitted_ep').verbose_name,
                              models.Layer._meta.get_field('number_format_A_ep').verbose_name,
                              models.Layer._meta.get_field('number_format_B_ep').verbose_name,
                              models.Layer._meta.get_field('tool_units_ep').verbose_name,
                              models.Layer._meta.get_field('units_g').verbose_name,
                              models.Layer._meta.get_field('zeroes_omitted_g').verbose_name,
                              models.Layer._meta.get_field('number_format_A_g').verbose_name,
                              models.Layer._meta.get_field('number_format_B_g').verbose_name,
                              models.Layer._meta.get_field('tool_units_g').verbose_name,
                              models.Layer._meta.get_field('status').verbose_name,
                              "标签",
                              "操作",
                              ]
        context['field_verbose_name'] = field_verbose_name# 表头用
        query=self.request.GET.get('query',False)
        if query:
            # context['cc'] = query
            # print(query)
            # context['query'] = query
            context['layers'] = models.Layer.objects.filter(
                Q(layer__contains=query) |
                Q(job__job_name__contains=query))
        return context

def view_layer(request,job_id):
    pass

    #找到job对象
    job=Job.objects.get(id=job_id)
    print(job.job_name,job.file_compressed)
    layers = models.Layer.objects.filter(job=job)

    field_verbose_name = [models.Layer._meta.get_field('job').verbose_name,
                          models.Layer._meta.get_field('layer').verbose_name,
                          models.Layer._meta.get_field('layer_org').verbose_name,
                          models.Layer._meta.get_field('vs_result_manual').verbose_name,
                          models.Layer._meta.get_field('vs_result_ep').verbose_name,
                          models.Layer._meta.get_field('vs_result_g').verbose_name,
                          models.Layer._meta.get_field('layer_file_type').verbose_name,
                          models.Layer._meta.get_field('layer_type').verbose_name,
                          models.Layer._meta.get_field('features_count').verbose_name,
                          models.Layer._meta.get_field('units_ep').verbose_name,
                          models.Layer._meta.get_field('zeroes_omitted_ep').verbose_name,
                          models.Layer._meta.get_field('number_format_A_ep').verbose_name,
                          models.Layer._meta.get_field('number_format_B_ep').verbose_name,
                          models.Layer._meta.get_field('tool_units_ep').verbose_name,
                          models.Layer._meta.get_field('units_g').verbose_name,
                          models.Layer._meta.get_field('zeroes_omitted_g').verbose_name,
                          models.Layer._meta.get_field('number_format_A_g').verbose_name,
                          models.Layer._meta.get_field('number_format_B_g').verbose_name,
                          models.Layer._meta.get_field('tool_units_g').verbose_name,
                          models.Layer._meta.get_field('status').verbose_name,
                          "标签",
                          "操作",
                          ]



    # return redirect('job_manage:LayerListView')
    return render(request, 'LayerListViewOneJob.html', {'field_verbose_name': field_verbose_name, 'layers': layers,'job':job})

class LayerUpdateView(UpdateView):
    """
    该类必须要有一个pk或者slug来查询（会调用self.object = self.get_object()）
    """
    model = models.Layer
    fields = "__all__"
    # template_name_suffix = '_update_form'  # html文件后缀
    template_name = 'LayerUpdateView.html'
    success_url = '../LayerListView' # 修改成功后跳转的链接

class LayerFormView(FormView):
    form_class = LayerFormsReadOnly
    template_name = "LayerFormView.html"
    def get(self, request, *args, **kwargs):
        layer = models.Layer.objects.filter(id=kwargs['parm']).first()
        form = self.form_class(instance=layer)
        return self.render_to_response({'form': form})

from .forms import LayerForm
class LayerUpdateViewOneJob(UpdateView):
    """
    该类必须要有一个pk或者slug来查询（会调用self.object = self.get_object()）
    """
    model = models.Layer
    fields = "__all__"
    # template_name_suffix = '_update_form'  # html文件后缀
    template_name = 'LayerUpdateView.html'

    def get(self, request, *args, **kwargs):
        global job_id
        layer_update = models.Layer.objects.get(id=self.kwargs['pk'])
        # initial = {'name': adv_positin.name}
        # form = self.form_class(initial)
        form=LayerForm(instance=layer_update)
        # print("*pk"*30,self.kwargs['pk'])
        self.job_id = layer_update.job_id


        return render(request, 'LayerUpdateView.html', {'form':form})

    #为什么不直接用success_url = '../view_layer/{}'.format(job_id)，因为这个job_id变量没办法把pk值同步过来 ，全局变量都 搞不定
    def get_success_url(self):
        return '../view_layer/{}'.format(self.object.job_id)
    # success_url = '../view_layer/{}'.format(job_id) # 修改成功后跳转的链接

def vs_ep(request,job_id):
    pass
    ep_vs_total_result_flag = True  # True表示最新一次悦谱比对通过
    vs_time=str(int(time.time()))

    print("悦谱VS",job_id)
    job = Job.objects.get(id=job_id)
    print(job.job_name, job.file_odb_current,job.file_odb_g)

    #拿到job_ep和job_g
    temp_path = r'C:\cc\share\temp'+"_"+str(request.user)+"_"+str(job_id)
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)
    if not os.path.exists(os.path.join(temp_path,'ep')):
        os.mkdir(os.path.join(temp_path,'ep'))
    if not os.path.exists(os.path.join(temp_path,'g')):
        os.mkdir(os.path.join(temp_path,'g'))

    job_ep_path=(os.path.join(settings.PROJECT_PATH,r'media',str(job.file_odb_current))).replace(r'/','\\')
    temp_ep_path=os.path.join(temp_path,'ep')
    shutil.copy(job_ep_path,temp_ep_path)
    time.sleep(0.2)
    ep_tgz_file = os.listdir(temp_ep_path)[0]
    print("ep_tgz_file:",ep_tgz_file)
    job_operation.untgz(os.path.join(temp_ep_path,str(job.file_odb_current).split('/')[-1]),temp_ep_path)
    if os.path.exists(os.path.join(temp_ep_path,str(job.file_odb_current).split('/')[-1])):
        os.remove(os.path.join(temp_ep_path,str(job.file_odb_current).split('/')[-1]))
    print("ep_tgz_file_now:",os.listdir(temp_ep_path)[0])

    job_g_path = (os.path.join(settings.PROJECT_PATH, r'media', str(job.file_odb_g))).replace(r'/', '\\')
    temp_g_path = os.path.join(temp_path, 'g')
    shutil.copy(job_g_path, temp_g_path)
    time.sleep(0.2)
    g_tgz_file = os.listdir(temp_g_path)[0]
    print("g_tgz_file:", g_tgz_file)
    job_operation.untgz(os.path.join(temp_g_path, str(job.file_odb_g).split('/')[-1]), temp_g_path)
    if os.path.exists(os.path.join(temp_g_path, str(job.file_odb_g).split('/')[-1])):
        os.remove(os.path.join(temp_g_path, str(job.file_odb_g).split('/')[-1]))
    print("g_tgz_file_now:", os.listdir(temp_g_path)[0])

    epcam.init()
    #打开job_ep
    # job_ep_name=str(job.file_odb_current).split('/')[-1][:-4]
    job_ep_name=os.listdir(temp_ep_path)[0]
    new_job_path_ep = os.path.join(temp_ep_path, job_ep_name)
    print("temp_ep_path:", temp_ep_path, "job_ep_name:", job_ep_name)
    res=job_operation.open_job(temp_ep_path, job_ep_name)
    print("open ep tgz:",res)
    print("job_ep_layer:", job_operation.get_all_layers(job_ep_name))
    if len(job_operation.get_all_layers(job_ep_name))==0:
        pass
        ep_vs_total_result_flag=False
        return HttpResponse("最新-EP-ODB++打开失败！！！！！")


    # 打开job_g
    # job_g_name = str(job.file_odb_g).split('/')[-1][:-4]
    job_g_name = os.listdir(temp_g_path)[0]
    new_job_path_g = os.path.join(temp_g_path, job_g_name)
    print("temp_g_path:", temp_g_path, "job_g_name:", job_g_name)
    job_operation.open_job(temp_g_path, job_g_name)
    print("open gp tgz:", res)
    print("job_g_layer:",job_operation.get_all_layers(job_g_name))
    if len(job_operation.get_all_layers(job_g_name))==0:
        pass
        ep_vs_total_result_flag=False
        return HttpResponse("G-ODB++打开失败！！！！！")



    tol = 0.9 * 25400
    isGlobal = True
    consider_sr = True
    map_layer_res = 200 * 25400
    all_result = {}  # 存放所有层比对结果


    step="orig"

    #原始层文件信息，最全的
    all_layer_from_org = models.Layer.objects.filter(job=job)
    print("all_layer_from_org:", all_layer_from_org)

    #以为悦谱解析好的为主，来VS
    all_layer = job_operation.get_all_layers(job_ep_name)
    print('悦谱tgz中的层信息：',all_layer)
    if len(all_layer)==0:
        pass

        ep_vs_total_result_flag = False


    for layer in all_layer:
        print("ep_layer:",layer)
        print("比对参数",job_ep_name, step, layer, job_g_name, step, layer, tol, isGlobal, consider_sr,map_layer_res)
        layer_result = epcam_api.layer_compare_point(job_ep_name, step, layer, job_g_name, step, layer, tol, isGlobal, consider_sr,map_layer_res)
        all_result[layer] = layer_result
        # for each in all_layer_org_from_org_file_list:
        #     if layer == str(each).lower():
        #         print("I find it!!!!!!!!!!!!!!")
        for each in all_layer_from_org:
            if layer == str(each.layer_org).lower():
                print("I find it!!!!!!!!!!!!!!")
                print(layer_result,type(layer_result))
                layer_result_dict=json.loads(layer_result)
                print(layer_result_dict)
                print(len(layer_result_dict["result"]))
                new_vs=models.Vs()
                new_vs.job=job
                new_vs.layer = each.layer
                new_vs.layer_org=each.layer_org
                new_vs.vs_result_detail=str(layer_result_dict)
                new_vs.vs_method='ep'
                new_vs.layer_file_type=each.layer_file_type
                new_vs.layer_type=each.layer_type
                new_vs.vs_time=vs_time
                try:
                    if len(layer_result_dict["result"])==0:
                        each.vs_result_ep='passed'
                        new_vs.vs_result ='passed'
                    if len(layer_result_dict["result"])>0:
                        each.vs_result_ep = 'failed'
                        new_vs.vs_result = 'failed'
                        ep_vs_total_result_flag=False
                except:
                    pass
                    print("异常！")
                each.vs_time=vs_time
                each.save()
                new_vs.save()
    pass
    if ep_vs_total_result_flag==True:
        pass
        job.vs_result_ep='passed'
    if ep_vs_total_result_flag==False:
        pass
        job.vs_result_ep='failed'
    job.vs_time=vs_time
    job.save()


    print("*" * 100)
    print(all_result)
    print("*" * 100)

    # 删除temp_path
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)

    # return HttpResponse("悦谱VS"+str(job_id))
    return redirect('job_manage:JobListView')


def vs_g(request,job_id):
    pass
    print("G软件VS",job_id)
    return HttpResponse("G软件VS"+str(job_id))

class VsListView(ListView):
    queryset = models.Vs.objects.all()
    # model=models.Job
    context_object_name = 'vs'
    paginate_by = 10
    # ordering = ['-publish']
    template_name = 'VsListView.html'

    # def get_queryset(self):
    #     query = self.request.GET.get('query', '')
    #     new_context = models.Job.objects.filter(
    #             Q(job_name__contains=query) |
    #             Q(author__username__contains=query))
    #     return new_context
    # def get_queryset(self):  # 重写get_queryset方法
    #     # 获取所有is_deleted为False的用户，并且以时间倒序返回数据
    #     return UserProfile.objects.filter(is_deleted=False).order_by('-create_time')

    def get_context_data(self, **kwargs):  # 重写get_context_data方法
        # 很关键，必须把原方法的结果拿到
        context = super().get_context_data(**kwargs)
        field_verbose_name = [models.Vs._meta.get_field('job').verbose_name,
                              models.Vs._meta.get_field('layer').verbose_name,
                              models.Vs._meta.get_field('layer_org').verbose_name,
                              models.Vs._meta.get_field('vs_result').verbose_name,
                              models.Vs._meta.get_field('vs_result_detail').verbose_name,
                              models.Vs._meta.get_field('vs_method').verbose_name,
                              models.Vs._meta.get_field('layer_file_type').verbose_name,
                              models.Vs._meta.get_field('layer_type').verbose_name,
                              models.Vs._meta.get_field('features_count').verbose_name,
                              models.Vs._meta.get_field('status').verbose_name,
                              models.Vs._meta.get_field('vs_time').verbose_name,
                              models.Vs._meta.get_field('create_time').verbose_name,
                              models.Vs._meta.get_field('updated').verbose_name,
                              "标签",
                              "操作",
                                  ]
        context['field_verbose_name'] = field_verbose_name# 表头用
        query=self.request.GET.get('query',False)
        if query:
            context['vs'] = models.Vs.objects.filter(
                Q(layer__contains=query) |
                Q(job__job_name__contains=query))
        return context

def view_vs(request,job_id):
    pass
    #找到job对象
    job=Job.objects.get(id=job_id)
    print(job.job_name,job.file_compressed)
    vs = models.Vs.objects.filter(job=job,vs_time=job.vs_time)

    field_verbose_name = [models.Vs._meta.get_field('job').verbose_name,
                          models.Vs._meta.get_field('layer').verbose_name,
                          models.Vs._meta.get_field('layer_org').verbose_name,
                          models.Vs._meta.get_field('vs_result').verbose_name,
                          models.Vs._meta.get_field('vs_result_detail').verbose_name,
                          models.Vs._meta.get_field('vs_method').verbose_name,
                          models.Vs._meta.get_field('layer_file_type').verbose_name,
                          models.Vs._meta.get_field('layer_type').verbose_name,
                          models.Vs._meta.get_field('features_count').verbose_name,
                          models.Vs._meta.get_field('status').verbose_name,
                          models.Vs._meta.get_field('vs_time').verbose_name,
                          models.Vs._meta.get_field('create_time').verbose_name,
                          models.Vs._meta.get_field('updated').verbose_name,
                          "标签",
                          "操作",
                          ]

    # return redirect('job_manage:LayerListView')
    return render(request, 'VsListViewOneJob.html', {'field_verbose_name': field_verbose_name, 'vs': vs,'job':job})

def view_vs_one_layer(request,job_id,layer_org):
    pass
    #找到job对象
    job=Job.objects.get(id=job_id)
    print(job.job_name,job.file_compressed)
    vs = models.Vs.objects.filter(job=job,vs_time=job.vs_time,layer_org=layer_org)

    field_verbose_name = [models.Vs._meta.get_field('job').verbose_name,
                          models.Vs._meta.get_field('layer').verbose_name,
                          models.Vs._meta.get_field('layer_org').verbose_name,
                          models.Vs._meta.get_field('vs_result').verbose_name,
                          models.Vs._meta.get_field('vs_result_detail').verbose_name,
                          models.Vs._meta.get_field('vs_method').verbose_name,
                          models.Vs._meta.get_field('layer_file_type').verbose_name,
                          models.Vs._meta.get_field('layer_type').verbose_name,
                          models.Vs._meta.get_field('features_count').verbose_name,
                          models.Vs._meta.get_field('drill_excellon2_units').verbose_name,
                          models.Vs._meta.get_field('drill_excellon2_zeroes_omitted').verbose_name,
                          # Job._meta.get_field('publish').verbose_name,
                          models.Vs._meta.get_field('drill_excellon2_number_format_A').verbose_name,
                          models.Vs._meta.get_field('drill_excellon2_number_format_B').verbose_name,
                          models.Vs._meta.get_field('drill_excellon2_tool_units').verbose_name,
                          models.Vs._meta.get_field('status').verbose_name,
                          models.Vs._meta.get_field('vs_time').verbose_name,
                          models.Vs._meta.get_field('create_time').verbose_name,
                          models.Vs._meta.get_field('updated').verbose_name,
                          "标签",
                          "操作",
                          ]

    # return redirect('job_manage:LayerListView')
    return render(request, 'VsListViewOneJob.html', {'field_verbose_name': field_verbose_name, 'vs': vs,'job':job})






def test(request):
    if request.user.is_authenticated:
        print(request.user.first_name,'|',request.user.username)
    return HttpResponse("abc")