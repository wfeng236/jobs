from django.db import models

# Create your models here.
class Hoteljob(models.Model):
    job_title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    job_description = models.TextField()
    experience = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    company_address = models.CharField(max_length=200)
    class Meta:
        db_table = 't_hoteljob'
