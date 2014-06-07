from django.db import models

# Create your models here.
# YO SANDRO WUZ HERE!!

class User(models.Model):
    name = models.CharField(max_length=200)
    account_number = models.CharField(max_length=50)
