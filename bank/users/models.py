from django.db import models

# Create your models here.

class UserAccount(models.Model):
    username = models.CharField(max_length=30,unique=True)
    password = models.CharField()
    def __str__(self):
        return self.username

class UserCard(models.Model):
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    useraccount = models.ForeignKey(UserAccount,on_delete=models.CASCADE,related_name='cards')
    def __str__(self):
        return f" {self.id}.{self.useraccount.username}"