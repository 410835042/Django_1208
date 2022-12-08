from django.db import models

# Create your models here.


class Search(models.Model):
    product_name = models.CharField(max_length=100)  # 戒指名稱
    brand = models.CharField(max_length=100)
