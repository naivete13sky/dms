from django.template import Library
import json
# 将注册类实例化为register对象
register =  Library()
# 使用装饰器注册
@register.filter
def get_drzl(val):
    # print(type(val))
    # result = json.loads(val)
    result=val["导入资料"]
    return result

@register.filter
def get_length_of_dict(val):

    result=len(val)
    return result

# @register.filter
# def get_length_of_dict2(val,key):
#
#     result=len(val)
#     return result