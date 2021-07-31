from django.db import models


# Create your models here.

class Addresses(models.Model):
    name = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=13)
    address = models.TextField()
    created = models.DateTimeField(auto_now_add=True)  # 데이터가 만들어 질때 시간을 알아서 입력

    class Meta:
        ordering = ['created']
