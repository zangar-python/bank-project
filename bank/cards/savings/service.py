from ..models import SavingMoney
from ..midleware import ifuserAuth
from users.models import UserAccount

from django.http import HttpResponse
from django.shortcuts import render,redirect

def createSaveMoney(request,card):
    if(request.method == 'POST'):
        if(not ifuserAuth(request)):
            return HttpResponse('U are not registering')
        user = UserAccount.objects.get(id=request.session['userid'])
        user_card =  user.cards.get(id=card)
        print(user_card)
        SavingMoney.objects.create(sum=0,card=user_card)
        return HttpResponse('created')
    else:
        return render(request,'./card/save_money_creating.html')

def savingsPage(request,card):
    if(not ifuserAuth(request)):
        return HttpResponse('U are not registering')
    user = UserAccount.objects.get(id=request.session['userid'])
    if(not user.cards.filter(id=card).exists()):
        return HttpResponse(f'карта с номером {card} не найден')
    user_card =  user.cards.get(id=card)
    # if(not ['saving'] in user_card):
    #     return HttpResponse('Вы еще не создали сохранение копитала')
    try:
        saving_balance = user_card.saving
    except Exception:
        print(Exception)
        return HttpResponse('Вы еще не создали сохранение копитала')
    return HttpResponse(saving_balance.sum)
    
def AddBalanceToSave(request,card):
    if(not ifuserAuth(request)):
        return HttpResponse('U are not registering')
    if(request.method != "POST"):
        return HttpResponse('Этот метод не используется в других целях')
    user = UserAccount.objects.get(id=request.session['userid'])
    if(not user.cards.filter(id=card).exists()):
        return HttpResponse(f'карта с номером {card} не найден')
    user_card = user.cards.get(id=card)
    
    try:
        card_saving = user_card.saving
    except Exception:
        return HttpResponse("Вы еще не создали капитал")    
    to_saving = request.POST['sum']
    
    if(to_saving == ""):
        return HttpResponse("Пополни поля")
    to_saving = int(to_saving)
    if(to_saving < 0):
        return HttpResponse('Минусовая сумма не принимается!')
    elif(to_saving > user_card.balance ):
        return HttpResponse('Не хватает средств')
    else:
        card_saving.sum += to_saving
        card_saving.save()
        user_card.balance -= to_saving
        user_card.save()
        return redirect(f'/card/{card}')
    

def fromSaveToCard(request,card):
    if(not ifuserAuth(request)):
        return HttpResponse('Вы не зарегестрировались')
    if(request.method != "POST"):
        return HttpResponse('Этот метод не используется в других целях.')
    user = UserAccount.objects.get(id=request.session['userid'])
    if(not user.cards.filter(id=card).exists()):
        return HttpResponse(f'Не найдено карты с номером {card}///')
    user_card = user.cards.get(id=card)
    try:
        card_saved = user_card.saving
    except Exception:
        return HttpResponse('У вас нету капитала.Сперва создадите ее.')
    to_get = request.POST['get']
    if(to_get == ""):
        return HttpResponse('Пополните поля')
    to_get = int(to_get)
    if(to_get < 0):
        return HttpResponse('Меньше нуля не принимается')
    elif to_get > card_saved.sum:
        return HttpResponse('Нехватает средств')
    else:
        user_card.balance += to_get
        user_card.save()
        card_saved.sum -= to_get
        card_saved.save()
        return redirect(f'/card/{card}')    