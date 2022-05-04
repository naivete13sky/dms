from django import forms
from django.contrib.auth.models import User
from .models import Carriage,Train,TrainSet

class CarriageFormsReadOnly(forms.ModelForm):
    class Meta:
        model = Carriage
        fields = '__all__'
        def __init__(self, *args, **kwargs):
            super(CarriageFormsReadOnly, self).__init__(*args, **kwargs)
            for name, field in self.fields.iteritems():
                field.widget.attrs['readonly'] = 'true'

class TrainFormsReadOnly(forms.ModelForm):
    class Meta:
        model = Train
        fields = '__all__'
        def __init__(self, *args, **kwargs):
            super(TrainFormsReadOnly, self).__init__(*args, **kwargs)
            for name, field in self.fields.iteritems():
                field.widget.attrs['readonly'] = 'true'

class TrainSetFormsReadOnly(forms.ModelForm):
    class Meta:
        model = TrainSet
        fields = '__all__'
        def __init__(self, *args, **kwargs):
            super(TrainSetFormsReadOnly, self).__init__(*args, **kwargs)
            for name, field in self.fields.iteritems():
                field.widget.attrs['readonly'] = 'true'
