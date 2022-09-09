from django.shortcuts import render
from django.views.generic.base import TemplateView
from job_manage.models import Job
from django.db.models import Avg,Max,Min,Count,Sum
from django.db import connection
import json
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
# Create your views here.
def index(request):
    return render(request,r'../templates/index.html')

def dashboard(request):

    job_counts=len(Job.objects.all())
    print(job_counts)
    job_published_counts=len(Job.objects.filter(status="published"))

    return render(request,r'dashboard.html',locals())


class DashBoardView(TemplateView):
    pass
    template_name = "DashBoardView.html"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)

        job_counts = len(Job.objects.all())
        context["job_counts"] = job_counts

        job_published_counts = len(Job.objects.filter(status="published"))
        context["job_published_counts"] = job_published_counts

        statics_author=Job.objects.values("author__username").annotate(c = Count("author")).order_by("-c")
        context["statics_author"] = statics_author
        context['field_verbose_name']=["负责人",'计数',"published料号数","draft料号数"]

        statics_author_list=[]
        for each in statics_author:
            pass
            one_author_tuple=(each["author__username"],each["c"])
            one_author_dict = {"负责人":each["author__username"],"料号数":each["c"],
                               "published料号数":len(Job.objects.filter(author__username=each["author__username"],status="published")),
                               "draft料号数":len(Job.objects.filter(author__username=each["author__username"],status="draft"))}
            # statics_author_list.append(one_author_tuple)
            statics_author_list.append(one_author_dict)

        context['statics_author_list'] = statics_author_list

        #每日新增料号数统计
        statics_day=Job.objects.values("create_time").annotate(c = Count("job_name")).order_by("-c")
        # print(statics_day)
        select = {'day': connection.ops.datetime_trunc_sql('day', 'create_time', 8)}
        result = Job.objects.extra(select=select).values('day').annotate(number=Count('id')).order_by("-day")[:7]
        x_list=[]
        y_list=[]
        for key in result:
            # print(key)
            x_list.append(str(datetime.date(key["day"])))

            y_list.append(key["number"])
        x_list.reverse()
        y_list.reverse()
        # print(x_list)
        # print(y_list)
        context['statics_job_by_day_x'] = json.dumps(x_list)
        context['statics_job_by_day_y'] = y_list


        #每日新增料号数统计，堆积柱状图
        today=datetime.date(datetime.now())
        # yestoday=datetime.date(datetime.now()) - relativedelta(days=1)
        # print("today:",today)
        # print("yestoday:", yestoday )
        def get_statics_job_by_day_author_list_n_day(author,n):
            statics_job_by_day_author_list_n_day=[]
            for each in range(0,n):
                pass
                # print(each)
                each_jobs=Job.objects.filter(author__username=author).filter(create_time__range=(today - relativedelta(days=each), today - relativedelta(days=each)+relativedelta(days=1)))
                each_job_count=len(each_jobs)
                # print("each_job_count:",each_job_count)

                statics_job_by_day_author_list_n_day.append(each_job_count)
            statics_job_by_day_author_list_n_day.reverse()
            return statics_job_by_day_author_list_n_day

        print("statics_job_by_day_author_list_7_day_cc:", get_statics_job_by_day_author_list_n_day("cc",7))
        context['statics_job_by_day_author_list_7_day_cc'] = get_statics_job_by_day_author_list_n_day("cc",7)
        print("statics_job_by_day_author_list_7_day_zjr:", get_statics_job_by_day_author_list_n_day("jinru.zhang", 7))
        context['statics_job_by_day_author_list_7_day_zjr'] = get_statics_job_by_day_author_list_n_day("jinru.zhang", 7)
        print("statics_job_by_day_author_list_7_day_gcc:", get_statics_job_by_day_author_list_n_day("congcong.guo", 7))
        context['statics_job_by_day_author_list_7_day_gcc'] = get_statics_job_by_day_author_list_n_day("congcong.guo", 7)
        print("statics_job_by_day_author_list_7_day_ze:", get_statics_job_by_day_author_list_n_day("en.zhu", 7))
        context['statics_job_by_day_author_list_7_day_ze'] = get_statics_job_by_day_author_list_n_day("en.zhu",7)
        print("statics_job_by_day_author_list_7_day_zzr:", get_statics_job_by_day_author_list_n_day("zhenru.zhao", 7))
        context['statics_job_by_day_author_list_7_day_zzr'] = get_statics_job_by_day_author_list_n_day("zhenru.zhao", 7)




        return context




def index_base_20220818(request):
    return render(request,r'../templates/index_base_20220818.html')