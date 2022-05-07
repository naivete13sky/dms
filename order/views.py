from django.db.models import Q
from django.shortcuts import render, redirect,HttpResponse
from django.urls import reverse_lazy

from .forms import CamOrderFormsReadOnly,CamOrderProcessFormsReadOnly

# Create your views here.
from django.views.generic import ListView, CreateView, FormView, UpdateView, DeleteView
from .models import CamOrder,CamOrderProcess
from process.models import Train,TrainSet,Carriage

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
                              CamOrder._meta.get_field('should_finish_time').verbose_name,
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

class CamOrderProcessListView_1(ListView):
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
                              # CamOrderProcess._meta.get_field('data').verbose_name,
                              CamOrderProcess._meta.get_field('author').verbose_name,
                              CamOrderProcess._meta.get_field('publish').verbose_name,
                              ]

        order_train=Train.objects.filter(name='CAM代工服务')[0]
        list_dynamic=[]
        #找到车头
        order_train_set_head=TrainSet.objects.filter(train=order_train,current_carriage__carriage_type='head')[0]
        field_verbose_name.append(Carriage.objects.filter(name=order_train_set_head.current_carriage.name)[0])
        list_dynamic.append(Carriage.objects.filter(name=order_train_set_head.current_carriage.name)[0].name)
        current_train_set_carriage=order_train_set_head
        # print("*" * 20, type(current_train_set_carriage), "*" * 20)
        #找到中间车厢
        while True:
            if current_train_set_carriage.post_carriage:
                # print("***1",current_train_set_carriage.post_carriage.name)
                field_verbose_name.append(Carriage.objects.filter(name=current_train_set_carriage.post_carriage.name)[0])
                list_dynamic.append(Carriage.objects.filter(name=current_train_set_carriage.post_carriage.name)[0].name)
                current_train_set_carriage=TrainSet.objects.filter(train=order_train,current_carriage__name=current_train_set_carriage.post_carriage.name)[0]
                # print("***2",current_train_set_carriage.name)
            else:
                break

        field_verbose_name.append("操作")
        context['field_verbose_name'] = field_verbose_name# 表头用

        context['list_dynamic']=list_dynamic
        context['list_input_status_select']=["审核通过","审核未通过"]
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


def input_status_select(request):
    if request.method == 'POST':
        selected=request.POST.get('input_status_select',None)
        id=request.POST.get('id',None)
        step = request.POST.get('step', None)
        # print(selected,id,step)
        object = CamOrderProcess.objects.filter(id=id)[0]
        # print("*"*100)
        # print(object)
        # print("*" * 100)
        print(object.data)
        dict_data=object.data
        print(type(dict_data))
        print(dict_data["导入资料"]["状态"])
        dict_data["导入资料"]["状态"]=selected
        object.data=dict_data
        object.save()
        print(object.data)
        # return redirect('project:ProjectListView')
        return HttpResponse("ok")
    # return render(request, 'factory_rule_select.html', locals())