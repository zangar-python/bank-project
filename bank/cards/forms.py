from django import forms

class Userform(forms.Form):
    username = forms.CharField()
    age = forms.IntegerField()
    