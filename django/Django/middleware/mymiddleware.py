
import time

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
# class MyMiddleWare(MiddlewareMixin):
#     def process_request(self, request):
#         print("中间件方法 process_request 被调用")
#     def process_view(self, request, callback, callback_args, callback_kwargs):
#         print("中间件方法 process_view 被调用")
#     def process_response(self, request, response):
#         print("中间件方法 process_response 被调用")
#         return response
#     def process_exception(self, request, exception):
#         print("中间件方法 process_exception 被调用")



class MyMiddleWare(MiddlewareMixin):
    pass
    # def process_request(self, request):
    #     # 获取客户端IP地址
    #     IP = request.META.get('REMOTE_ADDR')
    #     # 获取该IP地址的值，如果没有，给一个默认列表[]
    #     lis = request.session.get(IP, [])
    #     # 获取当前时间
    #     curr_time = time.time()
    #     # 判断操作次数是否小于3次
    #     if len(lis) < 3:
    #         # 如果小于3次,添加本次操作时间
    #         lis.append(curr_time)
    #         # 保存
    #         request.session[IP] = lis
    #     else:
    #         # 如果本次操作时间减去第一次操作时间小于60秒,则不让其继续操作
    #         if time.time() - lis[0] < 5:
    #             return HttpResponse('操作过于频繁')
    #         else:
    #             # 如果大于60秒则交叉复制
    #             lis[0], lis[1], lis[2] = lis[1], lis[2], time.time()
    #             # 保存
    #             request.session[IP] = lis