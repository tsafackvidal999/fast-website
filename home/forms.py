from django import forms

class LoginForm(forms.Form):
    username= forms.CharField(label="nom d'utilisateur",required=True,max_length=255   , widget=forms.TextInput(attrs={'class':'form-control mb-2'}))
    pwd=forms.CharField(label="mot de passe" ,required=True,max_length=255  ,   widget=forms.PasswordInput(attrs={'class':'form-control'}))


class Forms_GetAffilliationCode(forms.Form):
    code_affillie = forms.CharField(label='Choisissez votre code affillié',required=True,max_length=30,widget=forms.TextInput(attrs={'class':'form-control mb-2'}))
    nomber_of_free_days = forms.IntegerField(min_value=0, max_value= 60, required=True)


class ContactUsForm (forms.Form):
    name = forms.CharField(max_length=150, min_length=3,label="Nom", required=True)
    phone_number = forms.IntegerField(min_value= 650000000, max_value=699999999,label="Numero de téléphone", required=True)
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Entrez votre message ici...',
            'rows': 10,  # Nombre de lignes
            'cols': 40,  # Nombre de colonnes
            'class': 'form-control mb-2'  # Classe CSS pour le style
        }),
        label='message')