from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,r'../templates/index.html')

def dashboard(request):
    from job_manage.models import Job
    job_counts=len(Job.objects.all())
    print(job_counts)
    return render(request,r'dashboard.html',{"job_counts":job_counts})


def index_base_20220818(request):
    return render(request,r'../templates/index_base_20220818.html')