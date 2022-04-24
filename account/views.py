from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm,UserRegistrationForm,UserEditForm, ProfileEditForm,ProfileEditFormAll,FactoryRuleFormsReadOnly
from .models import Profile
from django.contrib import messages
from django.shortcuts import render, get_object_or_404,HttpResponse,redirect
from account import models
from.models import FactoryRule
from django.contrib.sites.models import Site
from django.views.generic import ListView,DetailView,FormView,CreateView
from django.db.models import Q

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authenticated successfully")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")

    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})

from django.contrib.auth.decorators import login_required
@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # 建立新数据对象但是不写入数据库
            new_user = user_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_form.cleaned_data['password'])
            # 保存User对象
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})

@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, "Error updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def profile_view(request):
    pass
    profile_list = models.Profile.objects.all()


    profile_field_verbose_name=[Profile._meta.get_field('user').verbose_name,
                            Profile._meta.get_field('mobile').verbose_name,
                            Profile._meta.get_field('recommender').verbose_name,
                            Profile._meta.get_field('cam_level').verbose_name,
                            "操作",
                            ]
    # print(job_field_verbose_name)

    #附件超链接
    current_site = Site.objects.get_current()
    # print(current_site)


    return render(request, r'../templates/profile_view.html',
                  {'profile_list': profile_list,
                   'profile_field_verbose_name':profile_field_verbose_name,
                   'current_site':current_site,
                   })

def add_profile(request):
    if request.method == "GET":
        # print("GET")
        user_form = UserRegistrationForm()
        # print(user_form)
        return render(request, 'add_profile.html', {'user_form': user_form})
    else:
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():  # 进行数据校验
            # 建立新数据对象但是不写入数据库
            new_user = user_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_form.cleaned_data['password'])
            # 保存User对象
            new_user.save()
            Profile.objects.create(user=new_user)

            up_status="新增完成！"
            return render(request, "add_profile_done.html", {'new_user': new_user})
        else:
            print(user_form.errors)    # 打印错误信息
            clean_errors = user_form.errors.get("__all__")
            print(222, clean_errors)
        return render(request, "add_profile.html", {"user_form": user_form, "clean_errors": clean_errors})

def edit_profile(request,id):
    profile = models.Profile.objects.filter(id=id).first()
    #获取修改数据的表单
    if request.method == "GET":
        form = ProfileEditFormAll(instance=profile)
        return render(request, r'profile_edit.html', locals())
    #POST请求添加修改过后的数据
    form = ProfileEditFormAll(data=request.POST,instance=profile)
    # print(form)
    status = ""
    #对数据验证并且保存
    if form.is_valid():
        # print("valid")
        form.save()
    # return HttpResponse('数据修改成功！！')
        status = "修改成功！"
    return render(request, r'profile_edit.html', {"status": status})

def del_profile(request, id):
    # print("abcedfg")
    profile = models.Profile.objects.filter(id=id).first()
    # print(profile)
    # 获取修改数据的表单
    if request.method == "GET":
        form = ProfileEditFormAll(instance=profile)
        return render(request, r'profile_delete.html', locals())
    if request.method == 'POST':
        profile.delete()
        return redirect('profile_view')

class FactoryRuleListView(ListView):
    queryset = models.FactoryRule.objects.all()
    # model=models.Job
    context_object_name = 'factoryrules'
    paginate_by = 10
    # ordering = ['-publish']
    template_name = r'factoryrules_view.html'
    def get_context_data(self, **kwargs):  # 重写get_context_data方法
        # 很关键，必须把原方法的结果拿到
        context = super().get_context_data(**kwargs)
        factoryrule_field_verbose_name = [FactoryRule._meta.get_field('factory_rule_name').verbose_name,
                                  FactoryRule._meta.get_field('remark').verbose_name,
                                  FactoryRule._meta.get_field('slug').verbose_name,
                                  FactoryRule._meta.get_field('author').verbose_name,
                                  FactoryRule._meta.get_field('publish').verbose_name,
                                  FactoryRule._meta.get_field('status').verbose_name,
                                  "操作",
                                  ]
        context['factoryrule_field_verbose_name'] = factoryrule_field_verbose_name# 表头用
        query=self.request.GET.get('query',False)
        if query:
            context['factoryrules'] = models.Job.objects.filter(
                Q(factory_rule_name__contains=query) |
                Q(author__username__contains=query))
        return context

class FactoryRuleFormView(FormView):
    form_class = FactoryRuleFormsReadOnly
    template_name = "detail_factoryrule.html"

    def get(self, request, *args, **kwargs):
        # print('get url parms: ' + kwargs['parm'])
        factoryrule = models.FactoryRule.objects.filter(id=kwargs['parm']).first()
        form = self.form_class(instance=factoryrule)
        return self.render_to_response({'form': form})

class FactoryRuleCreateView(CreateView):
    model=FactoryRule
    template_name = "factoryrule_create.html"
    # fields = ['factory_rule_name']
    fields = "__all__"
    success_url = 'FactoryRuleListView'
