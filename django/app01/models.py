from django.db import models

#用户表
class User(models.Model):
    user_id = models.AutoField(primary_key=True,verbose_name="用户ID")
    sex_choice = (
        (0, '女性'),
        (1, '男性'),
    )
    user_sex = models.IntegerField(choices=sex_choice, default=1)  # choices关键字固定的
    user_name = models.CharField(max_length=20,verbose_name="用户名")
    user_password = models.CharField(max_length=30,verbose_name="用户密码")
    user_phone = models.CharField(max_length=20,verbose_name="用户电话号码")
    user_email = models.EmailField(max_length=30,verbose_name="用户邮箱",null=True)


#管理员表
class Administrator(models.Model):
    Ad_id = models.AutoField(primary_key=True,verbose_name="管理员ID")
    Ad_name = models.CharField(max_length=20, verbose_name="管理员名")
    Ad_password = models.CharField(max_length=30, verbose_name="管理员密码")


#统计数据表
class Statistics(models.Model):
    user_ip = models.CharField(max_length=30,verbose_name="用户IP")
    user_brower = models.CharField(max_length=500,verbose_name="用户浏览器类型")
    date = models.DateTimeField(verbose_name="用户上线时间")


#用户应答信息表
class Answer_data(models.Model):
    data_id = models.AutoField(primary_key=True,verbose_name="特定数据id")
    key_words = models.CharField(max_length=30,verbose_name="关键字")
    reply = models.CharField(max_length=100,verbose_name="回复文字")
    user_image = models.ImageField(upload_to='media/',verbose_name="图片", null=True)
    url = models.CharField(max_length=100, verbose_name="超链接")

#用户上传信息表
class user_data(models.Model):
    id = models.AutoField(primary_key=True,verbose_name="输入数据id")
    words = models.CharField(max_length=30,verbose_name="用户输入的文字")
    image = models.ImageField(upload_to='upload/',verbose_name="用户上传的图片")