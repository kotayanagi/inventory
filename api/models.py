from django.db import models

# Create your models here.

class Stock(models.Model):

    name = models.CharField(max_length=255, verbose_name="商品名")
    price = models.IntegerField(default=0, verbose_name="価格")
    on_sale = models.BooleanField(default=False, verbose_name="販売中かどうか")
    stock = models.IntegerField(default=0, verbose_name="在庫")
    discount = models.IntegerField(default=0, verbose_name="値引き")


class Transaction(models.Model):

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name="商品")
    transaction_id = models.IntegerField(default=0, verbose_name="売買ID")
    discount = models.IntegerField(default=0, verbose_name="値引額")
    number = models.IntegerField(default=0, verbose_name="数")
    person = models.CharField(max_length=255, null=True, blank=True, verbose_name="担当者")