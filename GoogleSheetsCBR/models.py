from django.db import models

class ModelSort(models.Model):
    sorts_Model = models.CharField(max_length=30, default="№")
    ASC_DESK_Model = models.CharField(max_length=30, default="возрастанию")



