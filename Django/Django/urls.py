"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import: from my_app import views
    2. Add a URL to urlpatterns: path('', views. Home, name='home')
Class-based views
    1. Add an import: from other_app.views import Home
    2. Add a URL to urlpatterns: path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns: path('blog/', include('blog.urls'))
"""
#
# from django.conf import settings
#
# from django.contrib import admin
# from django.template.defaulttags import url
#
# from django.urls import path, re_path
# from django.views.static import serve
#
# import app01
#
# from app01 import views
#
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#
# from django.contrib.staticfiles.urls import static
# from . import settings
# from rest_framework.documentation import include_docs_urls

from django.conf import settings

from django.contrib import admin
from django.template.defaulttags import url

from django.urls import path, re_path
from django.views.static import serve

import app01

from app01 import views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib.staticfiles.urls import static
from . import settings
from django.urls import path

from rest_framework.documentation import include_docs_urls



urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('hello/',views.hello),
    # path('about/',MyView.as_view()),
    # path('zxa/',ProtectedView.as_view()),
    # path("user_list/", app01.views.user_list),
    # path("add_user/", app01.views.add_user),
    # path("edit_user/", app01.views.edit_user),
    # path("delete_user/", app01.views.delete_user),
    # path("user/forget/", app01.views.forget_password),
    path('user/list/', app01.views.user_list),
    path('user/add/', app01.views.add_user),
    path('user/delete/', app01.views.delete_user),
    path('user/<int:nid>/edit/', app01.views.edit_user),
    # path('user/resp/',app01.views.reset_password),
    path('admin/login/', views.admin_login),
    path('admin/register/', views.admin_register),
    path('admin/list/', views.admin_list),
    path('admin/add/', views.admin_add),
    path('admin/edit/', views.admin_edit),
    path('admin/delete/', app01.views.delete_admin),
    path("data/list/", app01.views.data_list),
    path("data/add/", app01.views.add_data),
    path("data/delete/", app01.views.delete_data),
    path("data/edit/", app01.views.edit_data),
    path('register/', app01.views.user_register),
    path('login/', app01.views.login),
    # path('reply/',app01.views.reply),
    path('get_Sta/', app01.views.getStatistic),
    path('high_word/', app01.views.order_highword),
    path('chart/pie/', app01.views.chart_pie),
    path('response/', app01.views.chatting),
    path('chat/',app01.views.chat),
    path('download/', app01.views.export_users_xls),
    path('gpt3-interaction/', app01.views.gpt3_interaction),
    # url(r'^docs/', include_docs_urls(title='API接口文档')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
