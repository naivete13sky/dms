from django import forms
from django.contrib.auth.models import User
from .models import CamOrder

class CamOrderFormsReadOnly(forms.ModelForm):
    class Meta:
        model = CamOrder
        fields = '__all__'
        def __init__(self, *args, **kwargs):
            super(CamOrderFormsReadOnly, self).__init__(*args, **kwargs)
            for name, field in self.fields.iteritems():
                field.widget.attrs['readonly'] = 'true'

