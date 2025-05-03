from users.models import UserAccount
def ifuserAuth(requests):
    if('userid' in requests.session):
        userid = requests.session.get('userid')
        if(not UserAccount.objects.filter(id=userid).exists()):
            del requests.session['userid']
            return False
        return True
    return False


from django.contrib.auth.hashers import make_password, check_password

def hashPassWord():
    password = "mypassword"
    hashed_password = make_password(password)  # Хэшируем пароль
    print(hashed_password)

    # Проверка пароля
    is_correct = check_password("mypassword", hashed_password)
    print(is_correct)  # True, если пароль совпадает

def addHashedPass(password:str):
    return make_password(password=password)

def isPAssAcces(password:str,hash_pass):
    return check_password(password,hash_pass)
    
    
    