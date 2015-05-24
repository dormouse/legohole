from django.db import models

class LegoSet(models.Model):
    number = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    add_datetime = models.DateTimeField(auto_now_add=True)
    modi_datetime = models.DateTimeField(auto_now=True)

class Vendor(models.Model):
    name = models.CharField(max_length=200)

class Discount(models.Model):
    legoset = models.ForeignKey(LegoSet)
    vendor = models.ForeignKey(Vendor)
    discount = models.IntegerField(default=0)

