from django.db import models

class Models(models.Model):
    number_Model = models.IntegerField()
    order_Model = models.IntegerField()
    value_dolar_Model = models.IntegerField()
    value_rub_Model = models.IntegerField()
    delivery_time_Model = models.DateTimeField()

class ModelSort(models.Model):
    sorts_Model = models.CharField(max_length=30, default="№")
    ASC_DESK_Model = models.CharField(max_length=30, default="возрастанию")



