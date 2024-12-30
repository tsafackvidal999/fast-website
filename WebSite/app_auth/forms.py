from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .multipleAccountWithUsername import create_unique_username

class LoginForm(forms.Form):
    username= forms.CharField(label="nom d'utilisateur",required=True,max_length=255   , widget=forms.TextInput(attrs={'class':'form-control mb-2'}))
    pwd=forms.CharField(label="mot de passe" ,required=True,max_length=255  ,   widget=forms.PasswordInput(attrs={'class':'form-control'}))

class registerForm(UserCreationForm):
    password1=forms.CharField(label="mot de passe" ,required=True ,max_length=255 ,   widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label="confirmez votre mot de passe" ,required=True,max_length=255  ,   widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', ]
        """ wiget = {
            'password': forms.PasswordInput(),
        } """
    """ username= forms.CharField(label="nom d'utilisateur",required=True  , widget=forms.TextInput(attrs={'class':'form-control mb-2'}))
    pwd=forms.CharField(label="mot de passe" ,required=True ,   widget=forms.PasswordInput(attrs={'class':'form-control'}))
    pwd_confirm=forms.CharField(label="confirmez votre mot de passe" ,required=True ,   widget=forms.PasswordInput(attrs={'class':'form-control'}))
    """
    def clean_password2(self) :
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2 :
            raise forms.ValidationError("Password don't match")
        return password2
    
    def save (self, comit = True):
        user = super().save()
        #user = super().save(comit = False)
        user.set_password(self.cleaned_data["password1"]) # Hash le mot de passe
        if comit:
            user.username = create_unique_username(user.username)
            user.save()
            return user
    

    