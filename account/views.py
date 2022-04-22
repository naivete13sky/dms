from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm,UserRegistrationForm,UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib import messages
from django.shortcuts import render, get_object_or_404,HttpResponse
from taggit.models import Tag
from account import models
from django.contrib.sites.models import Site

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
def profile_view(request,tag_slug=None):
    pass
    profile_list = models.Profile.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        profile_list = models.Job.objects.filter(tags__in=[tag])

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
                   'tag': tag
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

