from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy

from .models import Carriage,Train,TrainSet
# Create your views here.
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, FormView
from .forms import CarriageFormsReadOnly,TrainFormsReadOnly,TrainSetFormsReadOnly

class CarriageListView(ListView):
    queryset = Carriage.objects.all()
    context_object_name = 'all'
    paginate_by = 10
    # ordering = ['-publish']
    template_name = 'CarriageListView.html'
    def get_context_data(self, **kwargs):  # 重写get_context_data方法
        context = super().get_context_data(**kwargs)
        field_verbose_name = [Carriage._meta.get_field('name').verbose_name,
                                  Carriage._meta.get_field('remark').verbose_name,
                                  Carriage._meta.get_field('carriage_type').verbose_name,
                                  Carriage._meta.get_field('carriage_use').verbose_name,
                                  Carriage._meta.get_field('author_exe').verbose_name,
                                  Carriage._meta.get_field('check_set').verbose_name,
                                  Carriage._meta.get_field('author_check').verbose_name,
                                  Carriage._meta.get_field('author_create').verbose_name,
                                  Carriage._meta.get_field('publish').verbose_name,

                                  "操作",
                                  ]
        context['field_verbose_name'] = field_verbose_name# 表头用
        query=self.request.GET.get('query',False)
        if query:
            context['all'] = Carriage.objects.filter(
                Q(name__contains=query) |
                Q(carriage_use__contains=query))

        return context

class CarriageCreateView(CreateView):
    model=Carriage
    template_name = "CarriageCreateView.html"
    fields = "__all__"
    success_url = 'CarriageListView'

class CarriageDeleteView(DeleteView):
  model = Carriage
  template_name = 'CarriageDeleteView.html'
  # template_name_field = ''
  # template_name_suffix = ''
  # book_delete.html为models.py中__str__的返回值
   # namespace:url_name
  success_url = reverse_lazy('process:CarriageListView')

class CarriageUpdateView(UpdateView):
    """
    该类必须要有一个pk或者slug来查询（会调用self.object = self.get_object()）
    """
    model = Carriage
    fields = "__all__"
    # template_name_suffix = '_update_form'  # html文件后缀
    template_name = 'CarriageUpdateView.html'
    success_url = '../CarriageListView' # 修改成功后跳转的链接

class CarriageFormView(FormView):
    form_class = CarriageFormsReadOnly
    template_name = "CarriageFormView.html"
    def get(self, request, *args, **kwargs):
        carriage = Carriage.objects.filter(id=kwargs['parm']).first()
        form = self.form_class(instance=carriage)
        return self.render_to_response({'form': form})

class TrainListView(ListView):
    queryset = Train.objects.all()
    context_object_name = 'all'
    paginate_by = 10
    # ordering = ['-publish']
    template_name = 'TrainListView.html'
    def get_context_data(self, **kwargs):  # 重写get_context_data方法
        context = super().get_context_data(**kwargs)
        field_verbose_name = [Train._meta.get_field('name').verbose_name,
                                  Train._meta.get_field('remark').verbose_name,
                                  Train._meta.get_field('train_use').verbose_name,
                                  Train._meta.get_field('train_author_create').verbose_name,
                                  Train._meta.get_field('publish').verbose_name,
                                  "操作",
                                  ]
        context['field_verbose_name'] = field_verbose_name# 表头用
        query=self.request.GET.get('query',False)
        if query:
            context['all'] = Train.objects.filter(
                Q(name__contains=query) |
                Q(train_use__contains=query))

        return context

class TrainCreateView(CreateView):
    model=Train
    template_name = "TrainCreateView.html"
    fields = "__all__"
    success_url = 'TrainListView'

class TrainDeleteView(DeleteView):
  model = Train
  template_name = 'TrainDeleteView.html'
  # template_name_field = ''
  # template_name_suffix = ''
  # book_delete.html为models.py中__str__的返回值
   # namespace:url_name
  success_url = reverse_lazy('process:TrainListView')

class TrainUpdateView(UpdateView):
    """
    该类必须要有一个pk或者slug来查询（会调用self.object = self.get_object()）
    """
    model = Train
    fields = "__all__"
    # template_name_suffix = '_update_form'  # html文件后缀
    template_name = 'TrainUpdateView.html'
    success_url = '../TrainListView' # 修改成功后跳转的链接

class TrainFormView(FormView):
    form_class = TrainFormsReadOnly
    template_name = "TrainFormView.html"
    def get(self, request, *args, **kwargs):
        train = Train.objects.filter(id=kwargs['parm']).first()
        form = self.form_class(instance=train)
        return self.render_to_response({'form': form})

class TrainSetListView(ListView):
    queryset = TrainSet.objects.all()
    context_object_name = 'all'
    paginate_by = 10
    # ordering = ['-publish']
    template_name = 'TrainSetListView.html'
    def get_context_data(self, **kwargs):  # 重写get_context_data方法
        context = super().get_context_data(**kwargs)
        field_verbose_name = [TrainSet._meta.get_field('name').verbose_name,
                              TrainSet._meta.get_field('remark').verbose_name,
                              TrainSet._meta.get_field('order_id').verbose_name,
                              TrainSet._meta.get_field('train').verbose_name,
                              TrainSet._meta.get_field('pre_carriage').verbose_name,
                              TrainSet._meta.get_field('post_carriage').verbose_name,
                              TrainSet._meta.get_field('current_carriage_author_create').verbose_name,
                              TrainSet._meta.get_field('publish').verbose_name,
                              "操作",
                                  ]
        context['field_verbose_name'] = field_verbose_name# 表头用
        query=self.request.GET.get('query',False)
        if query:
            context['all'] = TrainSet.objects.filter(
                Q(name__contains=query) |
                Q(train__name__contains=query))

        return context

class TrainSetCreateView(CreateView):
    model=TrainSet
    template_name = "TrainSetCreateView.html"
    fields = "__all__"
    success_url = 'TrainSetListView'

class TrainSetDeleteView(DeleteView):
  model = TrainSet
  template_name = 'TrainSetDeleteView.html'
  # template_name_field = ''
  # template_name_suffix = ''
  # book_delete.html为models.py中__str__的返回值
   # namespace:url_name
  success_url = reverse_lazy('process:TrainSetListView')

class TrainSetUpdateView(UpdateView):
    """
    该类必须要有一个pk或者slug来查询（会调用self.object = self.get_object()）
    """
    model = TrainSet
    fields = "__all__"
    # template_name_suffix = '_update_form'  # html文件后缀
    template_name = 'TrainSetUpdateView.html'
    success_url = '../TrainSetListView' # 修改成功后跳转的链接

class TrainSetFormView(FormView):
    form_class = TrainSetFormsReadOnly
    template_name = "TrainSetFormView.html"
    def get(self, request, *args, **kwargs):
        train_set = TrainSet.objects.filter(id=kwargs['parm']).first()
        form = self.form_class(instance=train_set)
        return self.render_to_response({'form': form})