from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import ProjectFormsReadOnly,FactoryRuleFormsProjectNew
# Create your views here.
from django.views.generic import ListView, FormView, CreateView, UpdateView, DeleteView
from project import models
from .models import Project
from django.http import HttpResponse
from .models import FactoryRule
from django.contrib.auth.models import User


class ProjectListView(ListView):
    queryset = Project.objects.all()
    # model=models.Job
    context_object_name = 'all'
    paginate_by = 10
    # ordering = ['-publish']
    template_name = 'ProjectListView.html'
    def get_context_data(self, **kwargs):  # 重写get_context_data方法
        context = super().get_context_data(**kwargs)
        field_verbose_name = [Project._meta.get_field('name').verbose_name,
                                  Project._meta.get_field('org').verbose_name,
                                  Project._meta.get_field('work').verbose_name,
                                  Project._meta.get_field('author').verbose_name,
                                  Project._meta.get_field('create_time').verbose_name,
                                  Project._meta.get_field('updated').verbose_name,
                                  Project._meta.get_field('last_update_user').verbose_name,
                                  '厂规',
                                  Project._meta.get_field('customer_rule_status').verbose_name,
                                  Project._meta.get_field('create_type').verbose_name,
                                  Project._meta.get_field('status').verbose_name,
                                  Project._meta.get_field('remark').verbose_name,
                                  "操作",
                                  ]
        context['field_verbose_name'] = field_verbose_name# 表头用
        query=self.request.GET.get('query',False)
        if query:
            context['all'] = models.Project.objects.filter(
                Q(name__contains=query) |
                Q(author__username__contains=query))

        return context

class ProjectFormView(FormView):
    form_class = ProjectFormsReadOnly
    template_name = "ProjectFormView.html"

    def get(self, request, *args, **kwargs):
        # print('get url parms: ' + kwargs['parm'])
        project = models.Project.objects.filter(id=kwargs['parm']).first()
        form = self.form_class(instance=project)
        return self.render_to_response({'form': form})

class ProjectCreateView(CreateView):
    model=Project
    template_name = "ProjectCreateView.html"
    fields = "__all__"
    success_url = 'ProjectListView'

class ProjectUpdateView(UpdateView):
    """
    该类必须要有一个pk或者slug来查询（会调用self.object = self.get_object()）
    """
    model = Project
    fields = "__all__"
    # template_name_suffix = '_update_form'  # html文件后缀
    template_name = 'ProjectUpdateView.html'
    success_url = '../ProjectListView' # 修改成功后跳转的链接



class ProjectDeleteView(DeleteView):
  model = Project
  template_name = 'ProjectDeleteView.html'
  # template_name_field = ''
  # template_name_suffix = ''
  # book_delete.html为models.py中__str__的返回值
   # namespace:url_name
  success_url = reverse_lazy('project:ProjectListView')

def project_settings(request):
    pass
    return render(request, r'project_settings.html', locals())

def factory_rule_delete(request,pk):
    object = Project.objects.filter(id=pk)[0]
    if request.method == 'POST':
        object=Project.objects.filter(id=pk)[0]
        object.factory_rule=None
        object.save()
        # return HttpResponse("已删除!")
        # return render(request, r'factory_rule_delete.html', locals())
        return redirect('project:ProjectListView')
    return render(request, r'factory_rule_delete.html', locals())

def factory_rule_select(request,author_id,id):
    pass
    objects=FactoryRule.objects.filter(author=author_id)

    if request.method == 'POST':
        pass
        selected=request.POST.get('factory_rule_select',None)
        # print(selected)
        project = Project.objects.filter(id=id)[0]
        project.factory_rule = FactoryRule.objects.filter(factory_rule_name=selected)[0]
        project.save()
        return redirect('project:ProjectListView')
    return render(request, r'factory_rule_select.html', locals())

def factory_rule_new(request,author_id,id):
    print("author_id:",author_id,"id:",id)
    form=FactoryRuleFormsProjectNew()
    if request.method == 'POST':
        factory_rule_form = FactoryRuleFormsProjectNew(request.POST)
        if factory_rule_form.is_valid():
            # 建立新数据对象但是不写入数据库
            new_factory_rule = factory_rule_form.save(commit=False)
            # 保存User对象
            user=User(id=author_id)
            new_factory_rule.author=user
            new_factory_rule.save()

            project=Project.objects.filter(id=id)[0]
            project.factory_rule=new_factory_rule
            project.save()

        return redirect('project:ProjectListView')
    return render(request, r'factory_rule_new.html', locals())



