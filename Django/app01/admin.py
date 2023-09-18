from django.contrib import admin

# Register your models here.
from . import models
# admin.site.register(User)
from .models import User

# admin.site.register(models.User)
admin.site.register(models.Administrator)
admin.site.register(models.Answer_data)
admin.site.register(models.user_data)
admin.site.register(models.Statistics)

# from django.contrib import admin
#
# # # Register your models here.
# # Underwriter admin model
# class UserAdmin(admin.ModelAdmin):
#     # 需要显示的字段信息
#     list_display = ('user_id', 'user_name', 'user_password', 'user_phone','user_email')
#
#     # 设置哪些字段可以点击进入编辑界面，默认是第一个字段
#     list_display_links = ('user_id', 'user_name')
#
# # 注册时，在第二个参数写上 admin model
# admin.site.register(User, UserAdmin)
#
