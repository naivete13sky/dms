from django.template import Library
import json
# 将注册类实例化为register对象
register =  Library()
# 使用装饰器注册
@register.filter
def get_drzl(val):
    # print(type(val))
    # result = json.loads(val)
    try:
        result=val["导入资料"]
    except:
        result=""
    return result

@register.filter
def get_length_of_dict(val):
    result=len(val)
    return result

@register.filter
def get_dynamic(val,key):
    try:
        result=val[key]
    except:
        result=""
    return result