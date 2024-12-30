from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .calculate import NOMBRE_DE_MOIS_MAX_AUTORISER_POUR_LA_DEMANDE_DACTIVATION,NOMBRE_MAX_DE_PC_POUR_UNE_MEME_CLE_PRODUIT

class LoginForm(forms.Form):
    username= forms.CharField(label="nom d'utilisateur",required=True ,max_length=255 , widget=forms.TextInput(attrs={'class':'form-control mb-2'}))
    pwd=forms.CharField(label="mot de passe" ,required=True,max_length=255  ,   widget=forms.PasswordInput(attrs={'class':'form-control'}))


class  GetActivation(forms.Form):
    duration = forms.IntegerField(max_value=NOMBRE_DE_MOIS_MAX_AUTORISER_POUR_LA_DEMANDE_DACTIVATION, min_value=1, required= True)
    number_of_pc = forms.IntegerField(max_value=NOMBRE_MAX_DE_PC_POUR_UNE_MEME_CLE_PRODUIT, min_value=1, required= True)
    code_affillie = forms.CharField(label='Code promo(optionnel)',required=False,max_length=30,widget=forms.TextInput(attrs={'class':'form-control mb-2'}))
    payement_phone_number = forms.IntegerField(min_value=650000000,max_value=699999999,label='Numero MOMO ou OM pour le  payement', required=True,)

