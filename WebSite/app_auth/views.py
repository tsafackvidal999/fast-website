from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
#from django.contrib.auth.models import User
from .models import User
from django.contrib.auth.decorators import login_required
from time import time
from .multipleAccountWithUsername import search_the_user, check_if_the_user_exist_before_creation

from .forms import *

# Create your views here.

def last_login_blog(request):
    if request.method=="POST" :
        try:
            username=request.POST["username"]
            password=request.POST[ "pwd"]
            user=authenticate(username=username, password=password)
            if user is not None:
                print ("wellcome")
                login(request, user)
                #return redirect('home_index')
                return redirect('user_dashboard')
                #return render(request,'partials/user_dashboard.html')
            else:
                messages.error(request,"ERREUR D'AUTHENTIFICATION")
                return render(request,'login.html')
        except:
            messages.error(request,"ERREUR D'AUTHENTIFICATION")
            return render(request,'login.html')

    return render(request,'login.html')


def  last_search_the_user(small_username,pwd):

    users= User.objects.filter(username__contains = small_username)
    for user in users:
        #format du username  vidal|12345665432   (small_username|timespam)
        print(user.username,user.username.split('|'),user.password)
        if user.username.split('|')[0]==small_username and user.password == pwd:
            return user.username, pwd
    return small_username,pwd


def login_blog(request):
    messages_error=[]  
    username_valid=""
    userpwd_valid=""
    if request.method=="POST" :
        try:
            form=LoginForm(request.POST)
            if form.is_valid():
                username=form.cleaned_data['username']
                pwd=form.cleaned_data['pwd']
                username,pwd = search_the_user(username,pwd)
                print("username,pwd",username,pwd)
                user=authenticate(username=username,password=pwd)
                if user is not None:
                    print(user)
                    login(request, user)
                    #return redirect('home_index')
                    #return redirect('user_dashboard')
                    # Obtenez l'URL de redirection depuis 'next'
                    next_url = request.GET.get('next')
                    if next_url:
                        print('next_url',next_url)
                        return redirect(next_url)  # Redirige vers l'URL définie dans 'next'
                    else:
                        return redirect('user_dashboard')  # Redirige vers la page d'accueil (ou une autre page par défaut)
                        #return render(request,'partials/user_dashboard.html')
                else:
                    messages_error.append("Cet utilsateur n'a pas été trouvé")

                    return render(request,'login.html',{"form":form,"messages_error":messages_error})
            else:
                
                for field in form.errors:
                        form[field].field.widget.attrs['class'] += ' is-invalid'

                messages_error.append("le formulaire est invalide")

                if len(request.POST['username'])==0:
                    form[0].field.widget.attrs['class'] += ' is-invalid'

                    username_valid="Veuillez remplir ce champ"
                if len(request.POST['pwd'])==0:
                    form[1].field.widget.attrs['class'] += ' is-invalid'

                    userpwd_valid="Veuillez remplir ce champ"


                return render(request,'login.html',{"form":form,"messages_error":messages_error,'username_valid':username_valid,'userpwd_valid':userpwd_valid})
   
        except:
            messages.error(request,"ERREUR D'AUTHENTIFICATION")
            return render(request,'login.html')
    else:
        form=LoginForm(request.GET)
        return render(request,'login.html',{"form":form})



def register (request):
    messages_error=[]  
    if request.method == 'POST':
        try: 
            form=registerForm(request.POST, request.FILES)
            if form.is_valid():
                name = form.cleaned_data['username']
                pwd = form.cleaned_data['password1']
                pwd_confirm = form.cleaned_data['password2']
                if(name !="" and pwd!="" and pwd == pwd_confirm):
                    
                    try:
                        """ user = User.objects.create_user(username=name, password=pwd)
                        user.save() """
                        if check_if_the_user_exist_before_creation(name, pwd):
                            raise ValueError('this user is allready exist')
                        user = form.save()
                        if user is not None:
                            
                            login(request, user)
                            #return redirect('home_index')
                            return redirect('user_dashboard')
                            #return redirect("login_blog")
                        else :
                                messages_error.append("creation de compte echouée")
                                messages.error(request, "creation de compte echouée")
                            
                                return render(request,"register.html",{"form":form,"messages_error":messages_error})
                    except  Exception as e:
                        print(e)
                        messages_error.append("un compte existe déjà sous ce nom utilisateur veuilez le modifier")
                        messages.error(request,"un compte existe déjà sous ce nom utilisateur veuilez le modifier")
                elif pwd != pwd_confirm:
                    messages_error.append("les mots de passes ne sont pas identiques")
                elif name == "" or pwd == "" or pwd_confirm == "" :
                    messages_error.append("Veuillez remplir lse champs vides")
        except:
            messages_error.append("une erreur est survenu durant la création de votre compte")
        return render(request,"register.html",{"form": form,"messages_error":messages_error})
    form = registerForm()
    return render( request,"register.html", {"form": form,"messages_error":messages_error})


def logout_blog(request):
    logout(request)
    if not request.user.is_authenticated:
        print("l'utilisateur a été deconnecté")
    else:
        print("deconnexion echouée")
    return redirect("home_index")
