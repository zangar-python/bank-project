from django.contrib import admin

# Register your models here.
from users.models import UserAccount , UserCard
from .models import SavingMoney

admin.site.register(SavingMoney)
admin.site.register(UserCard)
admin.site.register(UserAccount)
