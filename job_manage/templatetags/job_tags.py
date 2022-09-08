from django import template
from ..models import Job,MyTag,TaggedWhatever
from django.db.models import Count, Q


register = template.Library()

@register.simple_tag(name='total_jobs')
def total_jobs():
    return Job.published.count()

@register.inclusion_tag('latest_jobs.html')
def show_latest_jobs(count=5):
    latest_jobs = Job.published.order_by('-publish')[:count]
    return {'latest_jobs': latest_jobs}

@register.simple_tag
def get_tags():
    return MyTag.objects.all()


@register.simple_tag
def get_tags_count():
    result = TaggedWhatever.objects.values('tag_id').order_by('tag_id').annotate(count=Count('tag_id'))
    tag_list=[]
    for each in result:
        print(each["tag_id"],each["count"])
        tag_one=MyTag.objects.get(id=each["tag_id"])
        tag_list.append((tag_one.name,tag_one.slug,each["count"]))

    return tag_list

