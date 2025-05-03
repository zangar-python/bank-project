from django.db import models

# Create your models here.

from users.models import UserCard

class SavingMoney(models.Model):
    created_at = models.DateField(auto_now_add=True)
    saved_at = models.DateTimeField(auto_now=True)
    sum = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    card = models.OneToOneField(UserCard,on_delete=models.CASCADE,related_name='saving')
    
    def __str__(self):
        return f'{self.card.id} savings balance={self.sum}'    