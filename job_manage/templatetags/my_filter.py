from django.template import Library
# 将注册类实例化为register对象
register =  Library()

# 使用装饰器注册
@register.filter
def replace(para1):
    # 替换
    result = str(para1).replace("job_manage","media")
    print(result)

    return result