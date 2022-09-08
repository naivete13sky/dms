from django.shortcuts import render
from django.views.generic.base import TemplateView
from job_manage.models import Job
from django.db.models import Avg,Max,Min,Count,Sum
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

        return context




def index_base_20220818(request):
    return render(request,r'../templates/index_base_20220818.html')