import random
import string
from faker import Faker
from app01.models import User


class CreatUsers(object):

    def __init__(self, count):
        self.count = count

    def creat_user(self):
        user_list = []
        fake = Faker("zh_CN")
        # str = ['139', '138', '137', '145', '154', '174', '150']
        for i in range(1, self.count):
            second = [3, 4, 5, 7, 8][random.randint(0, 4)]
            # 第三位数字
            third = {3: random.randint(0, 9),
                     4: [5, 7, 9][random.randint(0, 2)],
                     5: [i for i in range(10) if i != 4][random.randint(0, 8)],
                     7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
                     8: random.randint(0, 9), }[second]
            # 最后八位数字
            suffix = random.randint(9999999, 100000000)
            user_obj = User(user_name=fake.name(),
                            user_id=i,
                            user_email=''.join([random.choice(string.digits) for i in range(random.randint(8, 11))]) +
                                       random.choice(['@163.com', '@gmail.com', '@qq.com']),
                            user_password=''.join(random.sample(string.ascii_letters + string.digits, 8)),

                            user_sex=random.choice(['0', '1']),

                            user_phone="1{}{}{}".format(second, third, suffix),
                            # user_brower=''.join(random.choice(['chrome', 'edge', 'firefox'])),
                            )
            user_list.append(user_obj)
        User.objects.bulk_create(user_list)
        return user_list
