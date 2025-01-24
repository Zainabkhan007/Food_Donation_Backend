from django.db import models

from django.contrib.auth.hashers import make_password

# Create your models here.
class UserRegisteration(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    username=models.CharField(max_length=30)
    email=models.EmailField(max_length=254,unique=True)
    phone_no = models.IntegerField( blank=True, null=True)
    password=models.CharField(max_length=128)
    
    def save(self, *args, **kwargs):
      
        if self.password and (not self.pk or not UserRegisteration.objects.filter(id=self.pk, password=self.password).exists()):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.username   

class ContactUs(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(max_length=254)
    message=models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

       