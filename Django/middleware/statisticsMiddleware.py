
from django.utils.deprecation import MiddlewareMixin


from django.utils import timezone

from app01.models import Statistics


class statisticMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path in ['/login/']:
            # 获取客户端IP地址
            IP = request.META.get('REMOTE_ADDR')

            d1 = timezone.now()
            d2 = d1.strftime("%Y-%m-%d %H:%M:%S")
            brower = request.META['HTTP_USER_AGENT']
            Statistics.objects.create(user_ip= IP , user_brower=brower,date=d2)


