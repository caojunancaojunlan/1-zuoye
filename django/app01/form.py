

# from django import forms
# from django.core.validators import RegexValidator
# from django.forms import ModelForm
#
# from .models import Answer_data
#
# # class ImgForm(ModelForm):
# #     class Meta:
# #         model=Answer_data.user_image
#
#
#
# class PwdResetForm(forms.Form):
#     phoneNum = forms.CharField(label="手机号", widget=forms.TextInput(attrs={'class': 'form-control'}))
#     password1 = forms.CharField(
#         label="密码",
#         min_length=6,
#         max_length=20,
#         widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#         validators=[RegexValidator(r'^[^\s]+$', '密码不能包含空格')]
#     )
#
#     password2 = forms.CharField(
#         label="确认密码",
#         min_length=6,
#         max_length=20,
#         widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#         validators=[RegexValidator(r'^[^\s]+$', '密码不能包含空格')]
#     )
