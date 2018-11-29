import os
from datetime import datetime

import django
import random

# Create your tests here.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapy_django.settings')
django.setup()

from echarts_app import consts as c
from admin_app.models import User


def createUsers():
    for i in range(100000, 110000):
        User.objects.create(user_id='95588'+str(i), username='test'+str(i), time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), status=1, city=random.choice(c.PROVINCE))


