from django import forms
from django.contrib.auth.models import User
from .models import CamOrder,CamOrderProcess

class CamOrderFormsReadOnly(forms.ModelForm):
    class Meta:
        model = CamOrder
        fields = '__all__'
        def __init__(self, *args, **kwargs):
            super(CamOrderFormsReadOnly, self).__init__(*args, **kwargs)
            for name, field in self.fields.iteritems():
                field.widget.attrs['readonly'] = 'true'

class CamOrderProcessFormsReadOnly(forms.ModelForm):
    class Meta:
        model = CamOrderProcess
        fields = '__all__'
        def __init__(self, *args, **kwargs):
            super(CamOrderProcessFormsReadOnly, self).__init__(*args, **kwargs)
            for name, field in self.fields.iteritems():
                field.widget.attrs['readonly'] = 'true'

