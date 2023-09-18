from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from app01 import models


class repeatKeyWord(MiddlewareMixin):
    # db_data_list = [
    #         {"value": 1, "name": lcy},
    #         {"value": 5, "name": sxc},
    #         {"value": 2, "name": zcc},
    #     ]
    def process_request(self, request):
            db_data_list = []
            dict ={}
            if request.method == "POST":
                name = request.POST.get("user_name")
                user_list = models.User.objects.all()
                userName = []
                count = []
                for user_obj in user_list:
                    userName.append(user_obj.user_name)
                    for i in len(userName):
                        if userName[i]==name:
                            count[i] += 1
                        else:
                            userName.append(name)
                            count[i]=1
                    dict['value'] = count[i]
                    dict['name'] = userName[i]
                    db_data_list.append(dict)
                return db_data_list