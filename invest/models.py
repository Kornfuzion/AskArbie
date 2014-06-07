from django.db import models

# Create your models here.
# YO SANDRO WUZ HERE!!

class User(models.Model):
    name = models.CharField(max_length=200)
    account_number = models.CharField(max_length=50)

class RBC_Customer(models.Model):

    userName = models.CharField(max_length=200)
    income = models.PositiveIntegerField(u'income')
    
    investmentData_1 = models.FloatField(u'i_1')
    investmentData_2 = models.FloatField(u'i_2')
    investmentData_3 = models.FloatField(u'i_3')
    investmentData_4 = models.FloatField(u'i_4')
    investmentData_5 = models.FloatField(u'i_5')
    investmentData_6 = models.FloatField(u'i_6')
    investmentData_7 = models.FloatField(u'i_7')
    investmentData_8 = models.FloatField(u'i_8')
    investmentData_9 = models.FloatField(u'i_9')
    investmentData_10 = models.FloatField(u'i_10')
    investmentData_11 = models.FloatField(u'i_11')
    investmentData_12 = models.FloatField(u'i_12')
    investmentData_13 = models.FloatField(u'i_13')
    investmentData_14 = models.FloatField(u'i_14')
    investmentData_15 = models.FloatField(u'i_15')
    investmentData_12 = models.FloatField(u'i_16')
    investmentData_13 = models.FloatField(u'i_17')
    investmentData_14 = models.FloatField(u'i_18')
    investmentData_15 = models.FloatField(u'i_19')

    
    clusterID=models.PositiveIntegerField(u'clusterID')

