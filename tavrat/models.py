from django.db import models

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    kto = models.CharField(max_length=20)
    komu = models.CharField(max_length=20)
    poznamka = models.CharField(max_length=200)
    kolko = models.FloatField()
    datum = models.DateField()
    zmazane = models.BooleanField()