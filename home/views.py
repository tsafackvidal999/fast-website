from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import messages
from .models import Article , MyArticle,Cathegorie
from django.http import HttpResponse, Http404
import os
from django.contrib.auth.decorators import login_required
from .forms import Forms_GetAffilliationCode,ContactUsForm


from .models import Telechargement, MyAffilliates, ContactUs

def telecharger_fichier(request, fichier_id):
    # Récupérer l'objet Téléchargement correspondant à l'ID
    print("fichier_id:",fichier_id)
    telechargement = Telechargement.objects.get(id = fichier_id)
    #telechargement = get_object_or_404(Telechargement, id=fichier_id)
    print("telechargement:",telechargement)
    # Chemin vers le fichier
    chemin_fichier = telechargement.my_file.name
    print("chemin_fichier:",chemin_fichier)

    # Vérifier si le fichier existe
    if not os.path.exists(chemin_fichier):
        raise Http404("Fichier non trouvé.")
    print('ssssssssssssssssss')
    # Ouvrir le fichier en mode binaire
    print("telechargement.my_file.name.replace('static_download_files_','')",telechargement.my_file.name.replace('static/download/files/',''))
    with open(chemin_fichier, 'rb') as fichier:
        response = HttpResponse(fichier.read(), content_type='application')
        response['Content-Disposition'] = f'attachment; filename="{ telechargement.my_file.name.replace('static/download/files/','')}"'

        # Incrémenter le compteur de téléchargements
        telechargement.nombre_de_techargement += 1
        telechargement.save()  # Enregistrer le décompte

        return response

def page_telechargement(request):
    telechargements = Telechargement.objects.all()
    for telechargement in telechargements:
        telechargement.my_file.name = telechargement.my_file.name.split("/")[-1]
    return render(request, 'home/telechargement.html', {'telechargements': telechargements})


@login_required
def affilliation(request):


    messages_error=[]  
    if request.method == 'POST':
        try: 
            form=Forms_GetAffilliationCode(request.POST, request.FILES)
            if form.is_valid():
                code_affillie = form.cleaned_data['code_affillie']
                nomber_of_free_days = form.cleaned_data['nomber_of_free_days']
                if(code_affillie !="" ):
                    
                    try:
                        
                        if len(MyAffilliates.objects.filter(user = request.user)) != 0:
                            raise ValueError('this affliate is allready exist')
                        if len(MyAffilliates.objects.filter(code_affillie = code_affillie)) != 0:
                            print('This affilliate code allready exist')
                            messages_error.append("Ce code affillié est déjà utilisé.")
                            messages.error(request, "Ce code affillié est déjà utilisé.")
                        
                            return render(request,"home/Affiliation.html",{"form":form,"messages_error":messages_error})
                    
                        my_new_affilliate = MyAffilliates.objects.create(user = request.user, code_affillie = code_affillie, number_of_free_days = nomber_of_free_days)
                        my_new_affilliate.save()
                        if my_new_affilliate is not None:
                            
                            return redirect('user_dashboard')
                            #return redirect("login_blog")
                        else :
                                messages_error.append("Votre demande d'affilliation a echouée")
                                messages.error(request, "Votre demande d'affilliation a echouée")
                            
                                return render(request,"home/Affiliation.html",{"form":form,"messages_error":messages_error})
                    except  ValueError :
                        
                        messages_error.append("Vous êtes déjà affillié")
                        messages.error("Vous êtes déjà affillié")

                    except  Exception as e:
                        print(e)
                        messages_error.append("Une erreur est survenue durant votre de demande d'affilliation")
                        messages.error("Une erreur est survenue durant votre de demande d'affilliation")
                elif code_affillie == "" :
                    messages_error.append("Veuillez remplir lse champs vides")
        except :
            messages_error.append("une erreur est survenu durant la création de votre compte ")
        return render(request,"home/Affiliation.html",{"form": form,"messages_error":messages_error})
    form = Forms_GetAffilliationCode()
    return render( request,"home/Affiliation.html", {"form": form,"messages_error":messages_error})


def condictions_d_affilliation(request):
    return render(request,"home/condictons generales d affiliation.html")



def last_telecharger_fichier(request):
    # Spécifiez le chemin vers le fichier que vous souhaitez permettre le téléchargement
    fichier_path = os.path.join('chemin/vers/votre/fichier.zip')

    # Ouvrir le fichier en mode binaire
    with open(fichier_path, 'rb') as fichier:
        response = HttpResponse(fichier.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(fichier_path)
        return response




def contact_us(request):
    messages_error=[]  
    if request.method=="POST" :
        print('jjjjjjjjjjjjjjjjj')
        try:
            form=ContactUsForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                phone_number = form.cleaned_data['phone_number']
                message = form.cleaned_data['message']
                print('succesxzs save')
                print(name)
                print(phone_number, type(phone_number))
                print(message)
                if(name !="" and phone_number and message):
                    if (650000000<phone_number<699999999):
                        ContactUs.objects.create(
                            user = request.user if request.user.is_authenticated else None,
                            name = name,
                            phone_number = phone_number,
                            message = message
                        ).save()
                        print('succes save')
                        return render(request,"home/contact_us.html",{'contact_us_status':"Success", })
                    else:
                        print('dssssssssss')
                        
                        messages_error.append("Numéro de téléphone invalide")

                    
                else:
                    if name == '':
                        messages_error.append("nom invalid")
                    if not phone_number:
                        messages_error.append("Numéro de téléphone invalide")
                    if message == "":
                        messages_error.append("message invalide")

                    
                    return render(request,'home/contact_us.html',{"form":form,"messages_error":messages_error})
            else:
                
                for field in form.errors:
                        form[field].field.widget.attrs['class'] += ' is-invalid'

                messages_error.append("le formulaire est invalide")

                if len(request.POST['name'])==0:
                    form[0].field.widget.attrs['class'] += ' is-invalid'

                    
                if len(request.POST['message'])==0:
                    form[2].field.widget.attrs['class'] += ' is-invalid'

                    


                return render(request,'login.html',{"form":form,"messages_error":messages_error,})
   
        except:
            messages.error(request,"ERREUR DURRANT l'ENVOI DU MESSAGE")
            return render(request,'home/contact_us.html',{"form":form,"messages_error":messages_error,})

    else:
        print('kkkkkkkkkkkkkkk')

        form=ContactUsForm(request.GET)
        return render(request,'home/contact_us.html',{"form":form})






# Create your views here.
def home_index(request):
    

    return render(request,'home/home_index.html')

def download(request):
    return render(request,'home/download.html')


def article(request, id_article):

    try:
        myarticle=MyArticle.objects.get(id=id_article)
        print(myarticle.cathegorie)
        myarticle.nombre_de_vue +=1
        myarticle.save()
        articles_en_relations=MyArticle.objects.filter(cathegorie=myarticle.cathegorie)
        print(articles_en_relations) 
        return render(request,'home/article.html',{'myarticle':myarticle,'articles_en_relations': articles_en_relations})
        
    except:
      
        return render(request,'home/article_not_found.html') 




def search(request):
    #GET={"article":valeur}
    query=request.GET["article"]
    myarticles=MyArticle.objects.filter(title__icontains=query , desc__icontains=query)
   
    if  myarticles.count()!= 0:
        return render(request,'home/search.html',{"myarticles":myarticles})
    else:
        no_result='Aucun resultat pour votre recherhe << '+query+'>>'
        return render(request,'home/search.html',{'no_result':no_result})


def article_introuvable(request,chaine):
    return render(request,'home/article_not_found.html')


def sms(request):
    try:
        message=request.GET['body']
        message_splited=message.split("-")
        assert  len(message_splited) == 2
        title=message_splited[0]
        body=message_splited[1]

        cathegorie=Cathegorie.objects.get(id=4)
        myarticle=MyArticle(title=title,
                            desc=body,
                            cathegorie=cathegorie,
                            image="static/img/circuit.jpg,"
                            )
        myarticle.save()
        print("fin de l'enregistrement")
        result="DATAS SAVED SUCCESSFULY"
    except  AssertionError : 
        result=" DATA DON'T SAVED BECAUSE THE MESSAGE'S FORMAT IS INCORRECT "
    except   : 
        result="SAVE FAILLED"

    return render(request,'home/data_save_confirmation.html',{"result":result})


