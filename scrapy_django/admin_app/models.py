from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.CharField(max_length=20, db_column='user_id',primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    salt = models.CharField(max_length=10)
    time = models.CharField(max_length=20)
    status = models.CharField(max_length=11)
    city = models.CharField(max_length=100)
    class Meta:
        db_table = 't_users'