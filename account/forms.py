from django import forms
from django.contrib.auth.models import User
from .models import Profile,FactoryRule

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','first_name','email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError(r"Password don't match.")
        return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')

class ProfileEditFormAll(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

class ProfileFormsReadOnly(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        def __init__(self, *args, **kwargs):
            super(ProfileFormsReadOnly, self).__init__(*args, **kwargs)
            for name, field in self.fields.iteritems():
                field.widget.attrs['readonly'] = 'true'

class FactoryRuleFormsReadOnly(forms.ModelForm):
    class Meta:
        model = FactoryRule
        fields = '__all__'
        def __init__(self, *args, **kwargs):
            super(FactoryRuleFormsReadOnly, self).__init__(*args, **kwargs)
            for name, field in self.fields.iteritems():
                field.widget.attrs['readonly'] = 'true'

class FactoryRuleFormsProjectNew(forms.ModelForm):
    class Meta:
        model = FactoryRule
        # fields = '__all__'
        fields = ['factory_rule_name','remark','publish','status']


