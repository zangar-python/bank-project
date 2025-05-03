from users.models import UserAccount,UserCard

def authCard(id):
    if(UserAccount.objects.filter(id=id).exists()):
        user = UserAccount.objects.get(id=id)
        card = UserCard.objects.create(useraccount=user,balance=0.00)
        print(card.id)
        return card
    
    return False

def testCard(id):
    user = UserAccount.objects.get(id=id)
    cards = user.cards.all()
    for card in cards:
        card.balance += 10000
        card.save()
        print(card.useraccount.username,card.balance)
        
