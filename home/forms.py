from django import forms
from django.contrib.auth.models import User
import re


class UserRegisterForm(forms.Form):

    username = forms.CharField(label='Username',max_length=30, help_text="Dài từ 8-20 ký tự, không kết thức, bắt đầu hoặc chứa ký tự '.' hoặc '_'.")
    email = forms.EmailField(label='Email', widget=forms.EmailInput())
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(), help_text="Dài ít nhất 8 ký tự, có ít nhất 1 ký tự IN HOA, in thường, chữ số và ít nhất 1 ký tự đặc biệt.")
    password2 = forms.CharField(label='Re-Password', widget=forms.PasswordInput(), )

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search('^(?=[a-zA-Z0-9._]{8,20}$)(?!.*[_.]{2})[^_.].*[^_.]$', username):
            raise forms.ValidationError('Có cái đéo gì đó sai sai rồi!')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Username đã bị húp')

    def clean_password1(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            if re.search('^(?=.*[\w])(?=.*[\W])[\w\W]{8,}$', password1):
                return password1
            raise forms.ValidationError('Có cái đéo gì đó sai sai rồi!')

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
            else:
                raise forms.ValidationError('Có cái đéo gì đó sai sai rồi')

    def save(self):
        User.objects.create_user(username=self.cleaned_data['username'],
                                 email=self.cleaned_data['email'],
                                 password=self.cleaned_data['password2'],
                                 first_name=self.cleaned_data['first_name'],
                                 last_name=self.cleaned_data['last_name'])
