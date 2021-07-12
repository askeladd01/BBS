from django import forms
from django.contrib import auth

from user import models


class RegForm(forms.Form):
    username = forms.CharField(label='用户名', min_length=3, max_length=9, error_messages={
        'min_length': '用户名最少3位哦~',
        'max_length': '用户名最多9位哦~',
        'required': '用户名不能为空哦~'
    },
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': '请输入3-9位用户名'})
                               )
    password = forms.CharField(label='密码', min_length=6, max_length=32, error_messages={
        'min_length': '密码最少6位哦~',
        'max_length': '密码最多32位哦~',
        'required': '密码不能为空哦~'
    },
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': '请输入6-32位密码'})
                               )
    re_password = forms.CharField(label='确认密码', min_length=6, max_length=32, error_messages={
        'min_length': '密码最少6位哦~',
        'max_length': '密码最多32位哦~',
        'required': '确认密码不能为空哦~'
    },
                                  widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                    'placeholder': '请确认密码'})
                                  )

    email = forms.EmailField(label='邮箱', error_messages={
        'invalid': '请输入正确的邮箱格式',
        'required': '邮箱不能为空哦~'
    },
                             widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': '请输入邮箱'})
                             )
    verification_code = forms.CharField(label='验证码', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                        error_messages={'required': '验证码还没有填写哦~'})

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if models.UserInfo.objects.filter(username=username).exists():
            self.add_error('username', '用户名已存在')
        return username

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if not password == re_password:
            self.add_error('re_password', '两次输入密码不一致')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if models.UserInfo.objects.filter(email=email).exists():
            self.add_error('email', '此邮箱已被绑定')
        return email

    def clean_verification_code(self):
        code = self.request.session.get('注册账号', '')
        verification_code = self.cleaned_data.get('verification_code')
        if code and code == verification_code:
            return verification_code
        else:
            self.add_error('verification_code', '验证码错误')


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', error_messages={'required': '用户名或邮箱不能为空哦~'},
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': '请输入用户名或邮箱'})
                               )
    password = forms.CharField(label='密码', error_messages={'required': '密码不能为空哦~'},
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': '请输入密码'})
                               )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if models.UserInfo.objects.filter(username=username).exists():
            user = auth.authenticate(username=username, password=password)
            if user:
                self.cleaned_data['user'] = user
                return self.cleaned_data
            else:
                self.add_error('password', '密码错误')
        else:
            if models.UserInfo.objects.filter(email=username).exists():
                username = models.UserInfo.objects.get(email=username).username
                user = auth.authenticate(username=username, password=password)
                if user:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
                else:
                    self.add_error('password', '密码错误')
            else:
                self.add_error('username', '用户名或邮箱不存在')
        return self.cleaned_data


class SetPasswordForm(forms.Form):
    old_password = forms.CharField(label='原密码', min_length=6, max_length=32, error_messages={
        'required': '原密码不能为空哦~'
    },
                                   widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                     'placeholder': '请输入原密码'})
                                   )
    new_password = forms.CharField(label='新密码', min_length=6, max_length=32, error_messages={
        'min_length': '密码最少6位哦~',
        'max_length': '密码最多32位哦~',
        'required': '确认密码不能为空哦~'
    },
                                   widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                     'placeholder': '请输入新密码'})
                                   )
    re_password = forms.CharField(label='确认新密码', min_length=6, max_length=32, error_messages={
        'min_length': '密码最少6位哦~',
        'max_length': '密码最多32位哦~',
        'required': '确认密码不能为空哦~'
    },
                                  widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                    'placeholder': '请确认新密码'})
                                  )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            self.add_error('old_password', '原密码不正确')
        return old_password

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        old_password = self.cleaned_data.get('old_password')
        if old_password == new_password:
            self.add_error('new_password', '新密码与原密码不能相同')
        return new_password

    def clean_re_password(self):
        new_password = self.cleaned_data.get('new_password')
        re_password = self.cleaned_data.get('re_password')
        if new_password != re_password:
            self.add_error('re_password', '两次输入的密码不一致')
        return re_password


class ChangeNicknameForm(forms.Form):
    new_nickname = forms.CharField(label='新的昵称', max_length=15,
                                   widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入新的昵称'}),
                                   error_messages={'required': '新昵称不能为空'})

    def clean_new_nickname(self):
        new_nickname = self.cleaned_data['new_nickname']
        if models.UserInfo.objects.filter(nickname=new_nickname).exists():
            self.add_error('new_nickname', '昵称已被占用')
        return new_nickname


class BindEmailForm(forms.Form):
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    verification_code = forms.CharField(label='验证码', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                        error_messages={'required': '验证码还没有填写哦~'})

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean_verification_code(self):
        code = self.request.session.get('绑定邮箱', '')
        verification_code = self.cleaned_data.get('verification_code')
        if code and code == verification_code:
            return verification_code
        else:
            self.add_error('verification_code', '验证码错误')

    def clean_email(self):
        email = self.cleaned_data['email']
        if models.UserInfo.objects.filter(email=email).exists():
            self.add_error('email', '该邮箱已被绑定')
        return email


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入注册邮箱'}),
                             error_messages={'required': '邮箱还没有填写哦~'})
    verification_code = forms.CharField(label='验证码', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                        error_messages={'required': '验证码还没有填写哦~'})
    password = forms.CharField(label='新密码', min_length=8, max_length=32,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': '请输入8-32位新密码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgetPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not models.UserInfo.objects.filter(email=email).exists():
            self.add_error('email', '邮箱不存在')
        return email

    def clean_verification_code(self):
        code = self.request.session.get('忘记密码', '')
        verification_code = self.cleaned_data.get('verification_code')
        if code and code == verification_code:
            return verification_code
        else:
            self.add_error('verification_code', '验证码错误')