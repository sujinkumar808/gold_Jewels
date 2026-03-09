from django.db import models
from django.contrib.auth.models import User



class Products(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    img= models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        db_table ="Products" # use the exact collection name in Compass


class OTPLogin(models.Model):
    phone = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone

