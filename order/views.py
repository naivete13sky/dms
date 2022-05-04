from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import CamOrderFormsReadOnly,CamOrderProcessFormsReadOnly

# Create your views here.
from django.views.generic import ListView, CreateView, FormView, UpdateView, DeleteView
from .models import CamOrder,CamOrderProcess

class CamOrderListView(ListView):
    queryset = CamOrder.objects.all()
    context_object_name = 'all'
    paginate_by = 10
    # ordering = ['-publish']
    template_name = 'CamOrderListView.html'
    def get_context_data(self, **kwargs):  # 重写get_context_data方法
        context = super().get_context_data(**kwargs)
        field_verbose_name = [CamOrder._meta.get_field('name').verbose_name,
                                  CamOrder._meta.get_field('remark').verbose_name,
                                  CamOrder._meta.get_field('project').verbose_name,
                                  CamOrder._meta.get_field('customer_user').verbose_name,
                                  CamOrder._meta.get_field('customer_price').verbose_name,
                                  CamOrder._meta.get_field('process_user').verbose_name,
                                  CamOrder._meta.get_field('process_price').verbose_name,
                                  CamOrder._meta.get_field('author').verbose_name,
                                  CamOrder._meta.get_field('status').verbose_name,
                                  CamOrder._meta.get_field('process_times').verbose_name,
                                  CamOrder._meta.get_field('last_update_user').verbose_name,
                                  CamOrder._meta.get_field('cam_order_type').verbose_name,
                                  "操作",
                                  ]
        context['field_verbose_name'] = field_verbose_name# 表头用
        query=self.request.GET.get('query',False)
        if query:
            context['all'] = CamOrder.objects.filter(
                Q(name__contains=query) |
                Q(author__username__contains=query))

        return context

class CamOrderCreateView(CreateView):
    model=CamOrder
    template_name = "CamOrderCreateView.html"
    fields = "__all__"
    success_url = 'CamOrderListView'

class CamOrderDeleteView(DeleteView):
  model = CamOrder
  template_name = 'CamOrderDeleteView.html'
  # template_name_field = ''
  # template_name_suffix = ''
  # book_delete.html为models.py中__str__的返回值
   # namespace:url_name
  success_url = reverse_lazy('order:CamOrderListView')

class CamOrderUpdateView(UpdateView):
    """
    该类必须要有一个pk或者slug来查询（会调用self.object = self.get_object()）
    """
    model = CamOrder
    fields = "__all__"
    # template_name_suffix = '_update_form'  # html文件后缀
    template_name = 'CamOrderUpdateView.html'
    success_url = '../CamOrderListView' # 修改成功后跳转的链接

class CamOrderFormView(FormView):
    form_class = CamOrderFormsReadOnly
    template_name = "CamOrderFormView.html"
    def get(self, request, *args, **kwargs):
        cam_order = CamOrder.objects.filter(id=kwargs['parm']).first()
        form = self.form_class(instance=cam_order)
        return self.render_to_response({'form': form})

class CamOrderProcessListView(ListView):
    queryset = CamOrderProcess.objects.all()
    context_object_name = 'all'
    paginate_by = 10
    # ordering = ['-publish']
    template_name = 'CamOrderProcessListView.html'
    def get_context_data(self, **kwargs):  # 重写get_context_data方法
        context = super().get_context_data(**kwargs)
        field_verbose_name = [CamOrderProcess._meta.get_field('name').verbose_name,
                              CamOrderProcess._meta.get_field('remark').verbose_name,
                              CamOrderProcess._meta.get_field('cam_order').verbose_name,
                              CamOrderProcess._meta.get_field('data').verbose_name,
                              CamOrderProcess._meta.get_field('author').verbose_name,
                              CamOrderProcess._meta.get_field('publish').verbose_name,

                              "操作",
                                  ]
        context['field_verbose_name'] = field_verbose_name# 表头用
        query=self.request.GET.get('query',False)
        if query:
            context['all'] = CamOrderProcess.objects.filter(
                Q(name__contains=query) |
                Q(cam_order__name__contains=query))

        return context

class CamOrderProcessCreateView(CreateView):
    model=CamOrderProcess
    template_name = "CamOrderProcessCreateView.html"
    fields = "__all__"
    success_url = 'CamOrderProcessListView'

class CamOrderProcessDeleteView(DeleteView):
  model = CamOrderProcess
  template_name = 'CamOrderProcessDeleteView.html'
  # template_name_field = ''
  # template_name_suffix = ''
  # book_delete.html为models.py中__str__的返回值
   # namespace:url_name
  success_url = reverse_lazy('order:CamOrderProcessListView')

class CamOrderProcessUpdateView(UpdateView):
    """
    该类必须要有一个pk或者slug来查询（会调用self.object = self.get_object()）
    """
    model = CamOrderProcess
    fields = "__all__"
    # template_name_suffix = '_update_form'  # html文件后缀
    template_name = 'CamOrderProcessUpdateView.html'
    success_url = '../CamOrderProcessListView' # 修改成功后跳转的链接

class CamOrderProcessFormView(FormView):
    form_class = CamOrderProcessFormsReadOnly
    template_name = "CamOrderProcessFormView.html"
    def get(self, request, *args, **kwargs):
        train_set = CamOrderProcess.objects.filter(id=kwargs['parm']).first()
        form = self.form_class(instance=train_set)
        return self.render_to_response({'form': form})