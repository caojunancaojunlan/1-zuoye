import os
import re
from random import Random

from django.core.mail import send_mail
from django.http import JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from Django.settings import BASE_DIR, MEDIA_URL, MEDIA_ROOT, DEFAULT_FROM_EMAIL
from django.shortcuts import render, HttpResponse, redirect
from app01 import models
from django import forms
import openai


# from app01.form import PwdResetForm
from app01.utils.creat_user import CreatUsers
from app01.utils.pagination import Pagination


# 用户登录
class LoginForm(forms.Form):
    user_name = forms.CharField(label="用户名", widget=forms.TextInput, required=True)
    # 必填不能为空
    user_password = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True), required=True)


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功，获取到的用户名和密码
        # print(form.cleaned_data)

        # 去数据库校验数据
        # user_object=models.User.objects.filter(user_name=form.cleaned_data["user_name"])
        user_object = models.User.objects.filter(user_phone=form.cleaned_data['user_name'],
                                                 user_password=form.cleaned_data['user_password']

                                                 ).first()
        user_objects = models.User.objects.filter(user_email=form.cleaned_data['user_name'],
                                                  user_password=form.cleaned_data['user_password']

                                                  ).first()

        if not (user_object or user_objects):
            form.add_error("user_password", "用户名或密码错误")
            return render(request, "login.html", {'form': form})

        return render(request, 'resp.html', {'form': form})

    return render(request, "login.html", {'form': form})


from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


# 用户注册
class RegisterModelForm(forms.ModelForm):
    user_password = forms.CharField(label='密码', validators=[
        RegexValidator(r'^(?![0-9]+$)(?![a-zA-Z]+$)[a-zA-Z0-9]{6,20}', '密码必须是6-20位数字和字母组成')],
                                    widget=forms.PasswordInput(render_value=True), min_length=6, required=True,
                                    error_messages={"required": '请输入密码'})
    confirm_password = forms.CharField(label='确认密码', validators=[
        RegexValidator(r'^(?![0-9]+$)(?![a-zA-Z]+$)[a-zA-Z0-9]{6,20}', '密码必须是6-20位数字和字母组成')],
                                       widget=forms.PasswordInput(render_value=True), required=True,
                                       error_messages={"required": '请输入密码'})

    user_phone = forms.CharField(label='手机号',
                                 validators=[RegexValidator(r'^(1[2|3|4|5|6|7|8|9])\d{9}$', '手机号格式错误')],
                                 required=True,
                                 error_messages={"required": '请输入手机号'})

    user_email = forms.EmailField(label='邮箱', widget=forms.EmailInput(), required=True,
                                  error_messages={"required": '请输入邮箱'})
    user_name = forms.CharField(label="用户名", required=True, error_messages={"required": '请输入用户名'})

    class Meta:
        model = models.User
        # fields='__all__'
        fields = ["user_name", "user_sex", "user_email", "user_phone", "user_password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)

    def clean_confirm_password(self):
        print(self.cleaned_data)
        user_password = self.cleaned_data.get("user_password")
        confirm = self.cleaned_data.get("confirm_password")
        if user_password != confirm:
            raise ValidationError("密码不一致,请重新输入")
        # elif user_password!='/^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,16}$/':

        # raise ValidationError("密码格式不正确")
        return confirm


def user_register(request):
    if request.method == "GET":
        form = RegisterModelForm()
        return render(request, 'user_register.html', {'form': form})
    # 用户post提交数据，数据校验
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库中
        # print(form.cleaned_data)
        form.save()
        return redirect('/login/')

    # 校验失败，在页面显示错误信息
    return render(request, 'user_register.html', {"form": form})


from app01.models import Answer_data, User, Administrator


# 查询所有用户信息
def user_list(request):
    """创建用户"""
    # user = CreatUsers(30000)
    # user.creat_user()

    """用户列表"""

    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["user_name__contains"] = search_data

    queryset = User.objects.filter(**data_dict)

    """用户分页"""

    page_object = Pagination(request, queryset, page_size=20)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()

    context = {
        "search_data": search_data,

        "queryset": page_queryset,  # 分完页数据
        "page_string": page_string,  # 页码
    }

    return render(request, "user_list.html", context)


# 新增用户
@csrf_exempt
def add_user(request):
    """用户添加"""
    if request.method == "GET":
        context = {
            "gender_choice": User.sex_choice,
            "user": User.objects.all()
        }
        return render(request, 'user_add.html', context)
    user = request.POST.get("user")
    pwd = request.POST.get("pwd")
    id = request.POST.get("id")
    sex = request.POST.get("sex")
    phone = request.POST.get("phone")
    email = request.POST.get("email")
    User.objects.create(user_name=user, user_password=pwd, user_sex=sex, user_id=id, user_phone=phone,
                        user_email=email, )

    return redirect("/user/list/")


#
@csrf_exempt
def edit_user(request, nid):
    if request.method == "GET":
        sex_choice = User.sex_choice
        user_obj = User.objects.filter(user_id=nid).first()

        return render(request, 'user_edit.html', {"sex_choice": sex_choice, "user_obj": user_obj})
    user = request.POST.get("user")
    pwd = request.POST.get("pwd")
    # id = request.POST.get("id")
    sex = request.POST.get("sex")
    phone = request.POST.get("phone")
    email = request.POST.get("email")

    User.objects.filter(user_id=nid).update(user_name=user, user_password=pwd, user_sex=sex, user_phone=phone,
                                            user_email=email, )
    return redirect("/user/list/")


@csrf_exempt
def delete_user(request):
    """删除用户"""
    nid = request.GET.get('nid')
    User.objects.filter(user_id=nid).delete()
    # User.objects.all().delete()
    return redirect("/user/list/")


def delete_admin(request):
    """删除管理员"""
    nid = request.GET.get('nid')
    Administrator.objects.filter(Ad_id=nid).delete()
    return redirect("/admin/list/")


def data_list(request):
    # 查询数据库中的所有信息
    # data_list = models.Answer_data.objects.all()
    # return render(request,"data_list.html",{"data_list":data_list})
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["key_words__contains"] = search_data

    queryset = Answer_data.objects.filter(**data_dict)

    """分页"""

    page_object = Pagination(request, queryset, page_size=20)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()

    context = {
        "search_data": search_data,

        "queryset": page_queryset,  # 分完页数据
        "page_string": page_string,  # 页码
    }

    return render(request, "data_list.html", context)


def add_data(request):  # 封装
    if request.method == "GET":
        # 获取表单提交的内容
        context = {
            "data": Answer_data.objects.all()
        }
        return render(request, 'add_data.html', context)
    print(request.FILES)
    key_words = request.POST.get("key_words")
    reply = request.POST.get("reply")
    new_file = request.FILES['image']
    with open('media/' + new_file.name, 'wb+') as f:
        for chunk in new_file.chunks():
            f.write(chunk)
        f.close()
    user_image = new_file.name
    # new_file.save('MEDIA_URL'+'image')
    url = request.POST.get("url")
    # 保存到数据库
    models.Answer_data.objects.create(key_words=key_words, reply=reply, user_image=user_image,
                                      url=url)
    return redirect("/data/list/")


@csrf_exempt
def delete_data(request):
    # 1\获取要删除的id
    id = request.GET.get('id')
    # 2\根据id删除数据库中的记录
    del_data = models.Answer_data.objects.get(data_id=id)
    filepath = MEDIA_ROOT + '/' + str(del_data.user_image)
    os.remove(filepath)
    del_data.delete()
    return redirect("/data/list/")


def edit_data(request):
    data_id = request.GET.get('data_id')
    data_obj1 = models.Answer_data.objects.get(data_id=data_id)
    if request.method == "GET":
        return render(request, 'edit_data.html', {'data_obj1': data_obj1})
    else:  # 1获取表单提交过来的内容
        key_words = request.POST.get("key_words")
        reply = request.POST.get("reply")
        # image = request.POST.get("image")
        new_file = request.FILES['image']
        with open('media/' + new_file.name, 'wb+') as f:
            for chunk in new_file.chunks():
                f.write(chunk)
            f.close()
        image = new_file.name
        # new_file.save('MEDIA_URL'+'image')
        url = request.POST.get("url")
        # 2根据id 去数据库查找对象
        data_obj2 = models.Answer_data.objects.filter(data_id=data_id)
        # 3修改
        data_obj2.key_words = key_words
        data_obj2.reply = reply
        data_obj2.use_image = image
        models.Answer_data.objects.filter(data_id=data_id).update(key_words=key_words, reply=reply, user_image=image,
                                                                  url=url)
        # 4重定向到用户列表
        return redirect('/data/list/')


def order_highword(request):
    return render(request, "high_word.html")


def getStatistic(request):
    data_dict = {}
    if request.method == "POST":
        start = request.POST.get("date1", None)
        end = request.POST.get("date2", None)
        if start and end:
            obj = models.Statistics.objects.filter(date__range=(start, end))
        else:
            obj = models.Statistics.objects.all()
        page_object = Pagination(request, obj, page_size=20)
        page_queryset = page_object.page_queryset
        page_string = page_object.html()
        context = {

            "queryset": page_queryset,  # 分完页数据
            "page_string": page_string,  # 页码
        }
        return render(request, 'index.html', context)
    statistics_list = models.Statistics.objects.all()
    page_object = Pagination(request, statistics_list, page_size=20)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    context = {

        "queryset": page_queryset,  # 分完页数据
        "page_string": page_string,  # 页码
    }
    return render(request, "index.html", context)


def chart_pie(requset):
    # db_data_list = middleware.repeatKeyWord.repeatKeyWord
    data_list = models.user_data.objects.all()
    data = []
    dict = {}
    db_data_list = []
    for i in range(len(data_list)):
        data.insert(i, data_list[i].words)
    for data_item in data:
        if data_item in dict.keys():
            dict[data_item] = dict[data_item] + 1
        else:
            dict[data_item] = 1
    for key in dict:
        db_data_list.append({"value": dict[key], "name": key})
    result = {
        "status": True,
        "data": db_data_list
    }
    return JsonResponse(result)


def chatting(request):
    if request.method == 'GET':
        return render(request, "resp.html")
    else:
        pass


from django.http import JsonResponse
import openai


def chat_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        response = openai.ChatCompletion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=1024,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"]
        )
        return JsonResponse({'response': response['choices'][0]['text']})
    else:
        return JsonResponse({'error': 'Invalid request method'})
def chat(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}],
            max_tokens=1024,
            temperature=0.5,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"],
        )
        return render(request, 'chat.html', {'message': response.choices[0].text})
    else:
        return render(request, 'chat.html')


def admin_list(request):
    """管理员列表"""
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["Ad_name__contains"] = search_data
    queryset = Administrator.objects.filter(**data_dict)
    """分页"""
    page_object = Pagination(request, queryset, page_size=20)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()

    context = {
        "search_data": search_data,

        "queryset": page_queryset,  # 分完页数据
        "page_string": page_string,  # 页码
    }

    return render(request, "admin_list.html", context)


def admin_add(request):
    """管理员添加"""
    if request.method == "GET":
        context = {
            "admin": Administrator.objects.all()
        }
        widgets = {
            "pwd": forms.PasswordInput
        }

        return render(request, 'admin_add.html', context)
    admin = request.POST.get("admin")
    pwd = request.POST.get("pwd")
    Administrator.objects.create(Ad_name=admin, Ad_password=pwd)

    return redirect("/admin/list/")


def admin_edit(request):
    nid = request.GET.get('nid')
    """修改管理员"""

    if request.method == "GET":
        context = {

            "admin_obj": Administrator.objects.filter(Ad_id=nid).first()
        }

        return render(request, 'admin_edit.html', context)
    admin = request.POST.get("admin")
    pwd = request.POST.get("pwd")

    Administrator.objects.filter(Ad_id=nid).update(Ad_name=admin, Ad_password=pwd)
    return redirect("/admin/list/")


def admin_login(request):
    """管理员登录"""
    if request.method == 'GET':
        context = {
            "admin": Administrator.objects.all()
        }
        return render(request, 'admin_login.html', context)
    if request.method == 'POST':
        admin = request.POST.get('admin')
        pwd = request.POST.get('pwd')
        try:
            admin == Administrator.objects.get(Ad_name=admin)
            if pwd == Administrator.Ad_password:
                return redirect('#')
            else:
                error_msg = "密码错误"
                return render(request, "admin_login.html", {'error_msg': error_msg})
        except:
            error_msg = "用户名不存在"
            return render(request, "admin_login.html", {'error_msg': error_msg})
    return render(request, "admin_login.html")


# def admin_register(request):
#     """管理员注册"""
#     if request.method == 'POST':
#         admin_name = request.POST.get('admin_name')
#         admin_password = request.POST.get('admin_password')
#         admin_repassword = request.POST.get('admin_repassword')
#
#         try:
#             admin = Administrator.objects.get(Ad_name=admin_name)
#             if admin:
#                 msg = "管理员已存在"
#                 return render(request, 'admin_register.html', {'msg': msg})
#         except:
#             if admin_password != admin_repassword:
#                 error_msg = "密码不一致"
#                 return render(request, 'admin_register.html', {'error_msg': error_msg})
#             else:
#                 register = Administrator()
#                 register.Ad_name = admin_name
#                 register.Ad_password = admin_password
#                 register.save()
#                 return redirect('/admin/login/')
#     else:
#         return render(request, 'admin_register.html')

class Ad_RegisterModelForm(forms.ModelForm):
    Ad_name = forms.CharField(label="管理员名", required=True, error_messages={"required": '请输入管理员名名'})
    Ad_password = forms.CharField(label='密码', widget=forms.PasswordInput(render_value=True), min_length=3,
                                  max_length=10, required=True,
                                  error_messages={"required": '请输入密码'})
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput(render_value=True), required=True,
                                       error_messages={"required": '请输入密码'})

    class Meta:
        model = models.Administrator
        # fields='__all__'
        fields = ["Ad_name", "Ad_password", "confirm_password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)

    def clean_confirm_password(self):
        print(self.cleaned_data)
        Ad_password = self.cleaned_data.get("Ad_password")
        confirm = self.cleaned_data.get("confirm_password")
        if Ad_password != confirm:
            raise ValidationError("密码不一致,请重新输入")
            # elif admin_password!='/^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,16}$/':

            # raise ValidationError("密码格式不正确")
        return confirm


def admin_register(request):
    if request.method == "GET":
        form = Ad_RegisterModelForm()
        return render(request, 'admin_register.html', {'form': form})
    # 用户post提交数据，数据校验
    form = Ad_RegisterModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库中
        print(form.cleaned_data)
        form.save()
        return redirect('/admin/login/')

    # 校验失败，在页面显示错误信息
    return render(request, 'admin_register.html', {"form": form})


import xlwt
from django.http import HttpResponse


# 导出
def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['user_id', 'user_sex', 'user_name', 'user_password', 'user_phone', 'user_email']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = models.User.objects.all().values_list('user_id', 'user_sex', 'user_name', 'user_password', 'user_phone',
                                                 'user_email')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

# views.py

from django.http import JsonResponse
import requests

def gpt3_interaction(request):
    if request.method == 'POST':
        # 获取来自前端的请求数据，通常是文本数据
        input_text = request.POST.get('input_text')

        # 构建GPT-3.5 API请求
        api_key = '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'
        api_endpoint = 'https://api.openai.com/v1/engines/davinci-codex/completions'
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }
        data = {
            'prompt': input_text,
            'max_tokens': 50,  # 限制生成的最大标记数
        }

        # 发送POST请求到GPT-3.5 API
        response = requests.post(api_endpoint, headers=headers, json=data)

        if response.status_code == 200:
            # 解析GPT-3.5的响应
            gpt3_response = response.json()
            generated_text = gpt3_response['choices'][0]['text']

            # 返回生成的文本作为JSON响应
            return JsonResponse({'generated_text': generated_text})

    # 如果请求不是POST或处理失败，返回错误信息
    return JsonResponse({'error': 'Invalid request'}, status=400)
