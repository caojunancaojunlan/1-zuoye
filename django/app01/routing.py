#!/usr/bin/env python
# @Time:2022/9/27 10:01
# @Author:  小周
# @File:  routing.py
# @Software:  PyCharm
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from app01 import consumers

# 【channels】（第2步）设置默认路由在项目创建routing.py文件

from channels.routing import ProtocolTypeRouter, URLRouter

websocket_urlpatterns = [
    re_path(r'test/$', consumers.ChatConsumer.as_asgi())
]
