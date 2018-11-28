from django.db import models

# Create your models here.
class Hoteljob(models.Model):
    site = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    job_type = models.CharField(max_length=200)
    company_name = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    job_description = models.TextField()
    experience = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    company_address = models.CharField(max_length=200)
    format_salary = models.CharField(max_length=200)
    format_experience = models.CharField(max_length=200)
    class Meta:
        db_table = 't_hoteljob'
