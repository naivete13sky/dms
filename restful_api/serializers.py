'''需要创建TutorialSerializer类来管理序列化/反序列化Json数据。
 目标类需要继承至rest_framework.serializers.ModelSerializer。
 父类将自动获取字段集合和验证器
'''
from rest_framework import serializers
from restful_api.models import Tutorial


class TutorialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tutorial
        fields = ('id',
                  'title',
                  'description',
                  'published')