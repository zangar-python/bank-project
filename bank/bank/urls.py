"""
URL configuration for bank project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users.views import auth_user,delSession,delUsers,login,main,hashPAss
from cards.views import createCard,test,sideCard,addBalanceToCard,translate,index

from cards.savings.service import createSaveMoney,savingsPage , AddBalanceToSave,fromSaveToCard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',auth_user),
    path('del/',delSession),
    path('delu/',delUsers),
    path('login/',login),
    path('',main),
    path('card/',createCard),
    path('test/',test),
    path('card/<int:id>/',sideCard),
    path('card/<int:id>/add_balance/',addBalanceToCard),
    path('card/<int:from_id>/translate/',translate),
    path('hash/',hashPAss),
    path('index/',index),
    path('card/<int:card>/save/',createSaveMoney),
    path('card/<int:card>/saved/',savingsPage),
    path('card/<int:card>/saved/add/',AddBalanceToSave),
    path('card/<int:card>/save/get/',fromSaveToCard)
]
