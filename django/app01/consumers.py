# #!/usr/bin/env python
# # @Time:2022/9/27 9:42
# # @Author:小周
# # @File: consumers.py
# # @Software:PyCharm
# # 存储连接用户的地址，同ip可同时存在多用户，每一页面代表不同用户
# from datetime import datetime
#
# from channels.exceptions import StopConsumer
# from channels.generic.websocket import WebsocketConsumer
#
# from app01 import models as model
# import json
# from tencentcloud.common import credential
# from tencentcloud.common.profile.client_profile import ClientProfile
# from tencentcloud.common.profile.http_profile import HttpProfile
# from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# from tencentcloud.nlp.v20190408 import nlp_client, models
#
# CONN_LIST = []
#
#
# class ChatConsumer(WebsocketConsumer):
#     # 客户端向后端发送websocket请求时自动触发
#     def websocket_connect(self, message):
#         # 服务端允许和客户端创建连接
#         self.accept()
#         CONN_LIST.append(self)
#         # async_to_sync(self.channel_layer.group_add)('test111', self.channel_name)
#         print("connectionAccepted")
#
#     def websocket_receive(self, message):
#         # print(message['text'])
#         key_words = message['text']
#         model.user_data.objects.create(words=message['text'])
#
#         # if models.Answer_data.objects.filter(key_words=message['text']).first() is None:
#         #     for c in CONN_LIST:
#         #         c.send(key_words)
#         if model.Answer_data.objects.filter(key_words=message['text']):
#
#             t1 = "读取到关键字：" + message['text']
#             t2 = "返回短语：" + model.Answer_data.objects.filter(key_words=message['text']).first().reply
#
#             self.send(t1)
#             self.send(t2)
#
#         else:
#             try:
#                 # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey,此处还需注意密钥对的保密
#                 # 密钥可前往https://console.cloud.tencent.com/cam/capi网站进行获取
#                 cred = credential.Credential("AKIDmXDlFdu23zrdM1ZyGdCiElHifYKAsTxK", "MaiiccXL2c4Vp2BHk9TiqFY5X5Vp2894")
#                 # 实例化一个http选项，可选的，没有特殊需求可以跳过
#                 httpProfile = HttpProfile()
#                 httpProfile.endpoint = "nlp.tencentcloudapi.com"
#
#                 # 实例化一个client选项，可选的，没有特殊需求可以跳过
#                 clientProfile = ClientProfile()
#                 clientProfile.httpProfile = httpProfile
#                 # 实例化要请求产品的client对象,clientProfile是可选的
#                 client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile)
#
#                 # 实例化一个请求对象,每个接口都会对应一个request对象
#                 req = models.ChatBotRequest()
#                 params = {
#                     "Query": message['text']
#                 }
#                 req.from_json_string(json.dumps(params))
#
#                 # 返回的resp是一个ChatBotResponse的实例，与请求对象对应
#                 resp = client.ChatBot(req)
#                 # 输出json格式的字符串回包
#                 j = json.loads(resp.to_json_string())
#                 self.send(message['text'])
#                 self.send(j['Reply'])
#
#             except TencentCloudSDKException as err:
#                 print(err)
#
#     def websocket_disconnect(self, message):
#         # async_to_sync(self.channel_layer.group_discard)('test111',self.channel_name)
#         print(message['text'])
#         raise StopConsumer()

# !/usr/bin/env python
# @Time:2022/9/27 9:42
# @Author:小周
# @File:consumers.py
# @Software:PyCharm
# 存储连接用户的地址，同ip可同时存在多用户，每一页面代表不同用户
from datetime import datetime

from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer

from app01 import models as model
import json
import itchat
from turtle import clear
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models

from django.http import JsonResponse
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.tbp.v20190627 import tbp_client, models
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tbp.v20190627 import tbp_client, models

CONN_LIST = []


class ChatConsumer(WebsocketConsumer):
    # 客户端向后端发送websocket请求时自动触发
    def websocket_connect(self, message):
        # 服务端允许和客户端创建连接
        self.accept()
        CONN_LIST.append(self)
        # async_to_sync(self.channel_layer.group_add)('test111', self.channel_name)
        print("connectionAccepted")

    def websocket_receive(self, message):
        # print(message['text'])
        key_words = message['text']
        model.user_data.objects.create(words=message['text'])

        # if models.Answer_data.objects.filter(key_words=message['text']).first() is None:
        #     for c in CONN_LIST:
        #         c.send(key_words)
        if model.Answer_data.objects.filter(key_words=message['text']):

            t1 = "读取到关键字：" + message['text']
            t2 = "返回短语：" + model.Answer_data.objects.filter(key_words=message['text']).first().reply

            self.send(t1)
            self.send(t2)

        else:
            try:
                # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
                # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
                # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
                cred = credential.Credential("AKIDLZeXFLEvP6arvlNmxud7MO0OXTnmX4Xt", "IMHG4oOn01pRtBH9oJacIsGRyMZXGrLe")
                # 实例化一个http选项，可选的，没有特殊需求可以跳过
                httpProfile = HttpProfile()
                httpProfile.endpoint = "tbp.tencentcloudapi.com"

                # 实例化一个client选项，可选的，没有特殊需求可以跳过
                clientProfile = ClientProfile()
                clientProfile.httpProfile = httpProfile
                # 实例化要请求产品的client对象,clientProfile是可选的
                client = tbp_client.TbpClient(cred, "ap-guangzhou", clientProfile)

                # 实例化一个请求对象,每个接口都会对应一个request对象
                req = models.TextProcessRequest()
                params = {
                    "BotId": "d2b163de-faa0-4c01-b53a-5f59e2fb1a54",
                    "BotEnv": "release",
                    "InputText": "message['text']",
                    "TerminalId": "127.0.0.1:8000"

                    # "Query": message['text']
                }
                req.from_json_string(json.dumps(params))
                # 返回的resp是一个ChatBotResponse的实例，与请求对象对应
                # resp = client.TextProcess(req)
                #             # 输出json格式的字符串回包
                #             j = json.loads(resp.to_json_string())
                #             self.send(message['text'])
                #             self.send(j['Reply'])
                # except TencentCloudSDKException as err:
                #     print(err)

                # 返回的resp是一个TextProcessResponse的实例，与请求对象对应
                resp = client.TextProcess(req)
                # 输出json格式的字符串回包
                j = json.loads(resp.to_json_string())
                for i in j:
                    print(i)
                self.send(message['text'])
                self.send(j["ResponseMessage"]["GroupList"][0]["Content"])
                #return [j['Content']]
                print(resp.to_json_string())

            except TencentCloudSDKException as err:
                print(err)

            #     def chat_with_tbp(request):
            #         if request.method == 'GET':
            #             input_text = request.POST.get('input_text')
            #
            #             # 配置 TBP 客户端
            #             cred = credential.Credential("AKIDLZeXFLEvP6arvlNmxud7MO0OXTnmX4Xt", "IMHG4oOn01pRtBH9oJacIsGRyMZXGrLe")
            #             http_profile = HttpProfile()
            #             http_profile.endpoint = "tbp.tencentcloudapi.com"
            #             client_profile = ClientProfile()
            #             client_profile.httpProfile = http_profile
            #
            #             client = tbp_client.TbpClient(cred, "ap-guangzhou", client_profile)
            #
            #             # 创建 TBP 请求
            #             req = models.TextProcessRequest()
            #             req.BotId = 'd2b163de-faa0-4c01-b53a-5f59e2fb1a54'  # 您的 TBP 机器人 ID
            #             params = {
            #                 "Query": message['text']
            #             }
            #             req.from_json_string(json.dumps(params))
            #
            #             # 返回的resp是一个ChatBotResponse的实例，与请求对象对应
            #             resp = client.TextProcess(req)
            #             # 输出json格式的字符串回包
            #             j = json.loads(resp.to_json_string())
            #             self.send(message['text'])
            #             self.send(j['Reply'])
            # except TencentCloudSDKException as err:
            #     print(err)

            #             req.InputText = input_text
            #
            #             try:
            #                 # 发送请求到 TBP
            #                 resp = client.TextProcess(req)
            #                 answer = resp.Response
            #                 return JsonResponse({'answer': answer})
            #             except Exception as e:
            #                 return JsonResponse({'error': str(e)}, status=500)
            # except TencentCloudSDKException as err:
            #     return JsonResponse({'error': 'Invalid request'}, status=400)

    #             # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey,此处还需注意密钥对的保密
    #             # 密钥可前往https://console.cloud.tencent.com/cam/capi网站进行获取
    #             cred = credential.Credential("AKIDLZeXFLEvP6arvlNmxud7MO0OXTnmX4Xt", "IMHG4oOn01pRtBH9oJacIsGRyMZXGrLe")
    #             # 实例化一个http选项，可选的，没有特殊需求可以跳过
    #             httpProfile = HttpProfile()
    #             httpProfile.endpoint = "nlp.tencentcloudapi.com"
    #
    #             # 实例化一个client选项，可选的，没有特殊需求可以跳过
    #             clientProfile = ClientProfile()
    #             clientProfile.httpProfile = httpProfile
    #             # 实例化要请求产品的client对象,clientProfile是可选的
    #             client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile)
    #
    #             # 实例化一个请求对象,每个接口都会对应一个request对象
    #             req = models.ChatBotRequest()
    #             params = {
    #                 "Query": message['text']
    #                 # "Query": questionS
    #             }
    #             req.from_json_string(json.dumps(params))
    #
    #             # 返回的resp是一个ChatBotResponse的实例，与请求对象对应
    #             resp = client.ChatBot(req)
    #             print(resp.to_json_string())
    #             # 输出json格式的字符串回包
    #             j = json.loads(resp.to_json_string())
    #             # self.send(message['text'])
    #             # self.send(j['Reply'])
    #             return [j['Reply']]
    #
    #         except TencentCloudSDKException as err:
    #             print(err)
    #
    def websocket_disconnect(self, message):
        # async_to_sync(self.channel_layer.group_discard)('test111',self.channel_name)
        print(message['text'])
        raise StopConsumer()
