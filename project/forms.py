from django import forms
from django.contrib.auth.models import User
from .models import Project,FactoryRule

class ProjectFormsReadOnly(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        def __init__(self, *args, **kwargs):
            super(ProjectFormsReadOnly, self).__init__(*args, **kwargs)
            for name, field in self.fields.iteritems():
                field.widget.attrs['readonly'] = 'true'

class FactoryRuleFormsProjectNew(forms.ModelForm):
    class Meta:
        model = FactoryRule
        # fields = '__all__'
        fields = ['factory_rule_name','remark','publish','status']