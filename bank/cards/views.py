from django.shortcuts import render,redirect
from django.http import HttpResponse

from .midleware import ifuserAuth
from .service import authCard , testCard
from users.models import UserCard,UserAccount
# Create your views here.

from .forms import Userform
 
def index(request):
    userform = Userform()
    return render(request, "index.html", {"form": userform})

def createCard(requests):
    if(not ifuserAuth(requests)):
        return HttpResponse("вы не зарегестрировались")
    if(requests.method == 'GET'):
        return render(requests,'card/auth_card.html')
    card = authCard(id=(requests.session.get('userid')))
    if(card):
        return HttpResponse(f'card created,{card.id} ')
    return HttpResponse('err')
    
def test(requests):
    testCard(id=(requests.session.get('userid')))
    return HttpResponse('test')

# checkpoint нужно сделать систему пополнения перевода 

def sideCard(requests,id):
    if(not ifuserAuth(requests)):
        return HttpResponse("вы не зарегестрировались")
    ifExistCard = UserCard.objects.filter(id=id).exists()
    if(ifExistCard):
        card = UserCard.objects.get(id=id)
        userid = card.useraccount.id
        user_id_from_session = requests.session.get('userid')
        if(userid == user_id_from_session):
            try:
                is_saving_agree = card.saving
            except Exception:
                is_saving_agree = False
            return render(request=requests,template_name="card/card_page.html",context={"id":card.id,"sum":card.balance,"saving":is_saving_agree})
        else:
            return HttpResponse("Это страница вам недоступно!")
    return HttpResponse("Такой карточки не найдено")
        

def addBalanceToCard(requests,id):
    ifExistCard = UserCard.objects.filter(id=id).exists()
    if(ifExistCard):
        card = UserCard.objects.get(id=id)
        card.balance += 1000
        card.save()
        return redirect(f'/card/{id}')
    return HttpResponse("Такой карты не существует")

def translate(requests,from_id):
    if(requests.method != "POST"):
        return HttpResponse("Метод другой")
    if(not ifuserAuth(requests)):
        return HttpResponse("вы не зарегестрировались")
    user_id = requests.session['userid']
    user = UserAccount.objects.get(id=user_id)
    ifExistCard = user.cards.filter(id=from_id).exists()
    if(False == ifExistCard):
        return HttpResponse("Такой карточки не найдено")
    from_card = user.cards.get(id=from_id)
    balance = requests.POST.get("balance")
    if(balance == ""):
        return HttpResponse("Неправильные данные")
    balance = int(balance)
    if(balance<0):
        return HttpResponse("Неправильные данные")
    to_id = requests.POST.get("to")
    if(to_id == ""):
        return HttpResponse("Введите куда нужно переводит!")
    ifExistToIdCard = UserCard.objects.filter(id=to_id).exists()
    if(False == ifExistToIdCard):
        return HttpResponse("Такой карточки не найдено")
    to_card = UserCard.objects.get(id=to_id)
    if(int(to_id) == from_id):
        return HttpResponse("Одна и та же карта")
    if(from_card.balance >= balance):
        
        to_card.balance += balance
        
        to_card.save()
        from_card.balance -= balance
        from_card.save()
        return HttpResponse("Успешно переведено <a href='/' >Главная</a>")
    else:
        return HttpResponse("Ваш баланс не хватает")
    