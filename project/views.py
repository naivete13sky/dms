from django.db.models import Q
from django.shortcuts import render
from .forms import ProjectFormsReadOnly

# Create your views here.
from django.views.generic import ListView, FormView, CreateView, UpdateView, DeleteView

from project import models
from .models import Project


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
                                  Project._meta.get_field('factory_rule_status').verbose_name,
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

# class FactoryRuleCreateView(CreateView):
#     model=FactoryRule
#     template_name = "factoryrule_create.html"
#     # fields = ['factory_rule_name']
#     fields = "__all__"
#     success_url = 'FactoryRuleListView'
#
# class FactoryRuleUpdateView(UpdateView):
#     """
#     该类必须要有一个pk或者slug来查询（会调用self.object = self.get_object()）
#     """
#     model = FactoryRule
#     fields = "__all__"
#     # template_name_suffix = '_update_form'  # html文件后缀
#     template_name = 'factoryrule_update.html'
#     success_url = '' # 修改成功后跳转的链接
#
# class FactoryRuleDeleteView(DeleteView):
#   """
#   """
#   model = FactoryRule
#   template_name = 'factoryrule_delete.html'
#   # template_name_field = ''
#   # template_name_suffix = ''
#   # book_delete.html为models.py中__str__的返回值
#    # namespace:url_name
#   success_url = reverse_lazy('FactoryRuleListView')