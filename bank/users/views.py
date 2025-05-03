from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from users.models import UserAccount

from cards.midleware import hashPassWord,isPAssAcces,addHashedPass

from cards.midleware import ifuserAuth
# Create your views here.

def auth_user(requests):
    if('userid' in requests.session):
        return HttpResponse("ты уже аутентефекицировалься")
    elif(requests.method == 'GET'):
        messages.info(requests,"Напишите имя пользователья и пaроль в безопасном месте!")
        return render(requests,"auth/auth.html")
        # return HttpResponse("get")
    elif(requests.method == 'POST'):
        username = requests.POST.get("username","user")
        password = requests.POST.get("password","pass")
        if(UserAccount.objects.filter(username=username).exists()):
            messages.error(requests,"Имя пользователья уже занято")
            return render(requests,"auth/auth.html")
        hashed_pass = addHashedPass(password)
        user = UserAccount.objects.create(username=username,password=hashed_pass)
        user.save()
        requests.session['userid'] = user.id
        print(user.username,user.password,user.id)
        
        # cards = user.usercard_set.all()  
        # for card in cards:
        #     print(card.id)
        return HttpResponse(f'username : {username} ; password : {hashed_pass}')
    else:
        messages.error(requests,"Повторите попытку в этом месте!")
        return render(requests,"auth/auth.html")

def delSession(requests):
    if('userid' in requests.session):
        del requests.session['userid']
        return HttpResponse('удалено')
    return HttpResponse("ты еблан у тебя нету сессий")

def delUsers(requests):
    UserAccount.objects.all().delete()
    return HttpResponse("Удалено")

def login(requests):
    if('userid' in requests.session):
        return HttpResponse("ты уже аутентефекицировалься")
    elif(requests.method == 'GET'):
        # messages.info(requests,"Напишите имя пользователья и пaроль в безопасном месте!")
        return render(requests,"auth/login.html")
    # return HttpResponse("get")
    elif(requests.method == 'POST'):
        username = requests.POST.get('username','user')
        password = requests.POST.get('password','pass')
        if(UserAccount.objects.filter(username=username).exists()):
            user = UserAccount.objects.get(username=username)
            hash_pass = user.password
            if (isPAssAcces(password,hash_pass) is not True):
                return HttpResponse("Пользователь с таким именем и паролем не существует!")
            
            requests.session['userid'] = user.id
            return HttpResponse(f'hello {user.username}')
        else:
            return HttpResponse("Неправильно")
    else:
        return HttpResponse("error")


def main(requests):
    registered = False
    if(ifuserAuth(requests)):
        registered = True
        userid = requests.session.get('userid')
        if(UserAccount.objects.filter(id=userid).exists):
            user = UserAccount.objects.get(id=userid)
            cards = user.cards.all()
            return render(requests,"main.html",{'registered':registered,'username':user.username,'cards':cards})
        else:
            return render(requests,"main.html",{'registered':registered})
    return render(requests,"main.html",{'registered':registered})
        
    

def hashPAss(requests):
    hashPassWord()
    return HttpResponse("acces")