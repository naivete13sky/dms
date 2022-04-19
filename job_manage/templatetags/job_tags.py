from django import template
from ..models import Job

register = template.Library()

@register.simple_tag(name='total_jobs')
def total_jobs():
    return Job.published.count()

@register.inclusion_tag('latest_jobs.html')
def show_latest_jobs(count=5):
    latest_jobs = Job.published.order_by('-publish')[:count]
    return {'latest_jobs': latest_jobs}