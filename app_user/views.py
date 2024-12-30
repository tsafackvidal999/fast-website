from django.shortcuts import render, redirect
from home.models import MyArticle ,MyAffilliates
from activation.models import Activation
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from app_auth.multipleAccountWithUsername import    clean_username
from .models import RetraitAffilie

from dateutil.relativedelta import relativedelta



# Create your views here.
@login_required
def dashboard(request):
    context= dict()
    my_activations = Activation.objects.filter(user= request.user)
    
    for my_activation in my_activations:
        my_date = my_activation.date_de_payement
        my_date = date(my_date.year,my_date.month,my_date.day)
       #print(date.today())
        if (my_activation.small_date_de_payement + relativedelta(months=my_activation.who_many_months))< date.today():
           if my_activation.is_expirated != Activation.Statut.EXPIREE:
                my_activation.is_expirated = Activation.Statut.EXPIREE
                my_activation.save()
        
    context["my_activations"]= my_activations


    my_affilliate_objet = MyAffilliates.objects.filter(user = request.user).first()
    if my_affilliate_objet is not None:
        Mes_ventes = Activation.objects.filter(affilliate = my_affilliate_objet)
        context['Mes_ventes'] = Mes_ventes
        context['my_affillie_code'] = my_affilliate_objet.code_affillie
        total_ventes = 0
        for vente in Mes_ventes:
            total_ventes += vente.somme_gagner_par_l_affilie 

        context['total_ventes'] = total_ventes
        context['solde'] = my_affilliate_objet.solde
    try:
      # Préparer les labels et les données
        labels = list()
        data = list()
        is_he_new_client = list()
        for vente in Mes_ventes:
            my_date = vente.date_de_payement
            labels.append(datetime(my_date.year,my_date.month,my_date.day,my_date.hour,my_date.minute).strftime('%Y-%m-%d %H:%M'))
            #labels.append(str(datetime(my_date.year,my_date.month,my_date.day,my_date.hour,my_date.minute)))
            #labels.append(my_date.minute)
            data.append(vente.somme_gagner_par_l_affilie)
            """ labels.append(datetime(my_date.year,my_date.month,my_date.day,my_date.hour,my_date.minute).strftime('%Y-%m-%d %H:%M'))
            data.append(vente.somme_gagner_par_l_affilie) """
            is_he_new_client.append(int(vente.is_he_a_new_client_client_for_this_affilliate))

        print(labels)
        print(data)
        # on recherche les dates iedntique pour additionner leurs cout
        """ final_label = list()
        final_data = list()
        for i, lb in enumerate(labels):
            print(i,lb)
            if lb in final_label:

                index = final_label.index(lb)
                print("dd", final_data[index], index)
                final_data[index] += data[i] 
                print("dd", final_data[index])
            else:
                final_data.append(data[i])
                final_label.append(lb)
            
            print(final_label)
            print(final_data)
        

        print(final_label)
        print(final_label)
        
        data = final_label
        labels = final_data """
        
        print('ll',labels)
        print('data',data)
        context['labels'] = labels
        context['data'] = data
        context['is_he_new_client'] = is_he_new_client
    except Exception as e:
        print("dashboard() except code 01:",e)
    context['cleanned_username'] = clean_username(request.user.username)
    
    try:
        Mes_retraits = RetraitAffilie.objects.filter(affiliete = MyAffilliates.objects.get(user = request.user))
    
        total_retrait = 0
        for retrait in Mes_retraits:
            if retrait.status == RetraitAffilie.Status.PAYE:
                total_retrait += retrait.amount 

        context["total_retrait"] = total_retrait
        context["Mes_retraits"] = Mes_retraits
    
    except Exception as e:
        print(("exception in dashboard zdjkbdzekj",e))

    return render(request,'partials/user_dashboard.html',context=context)

@login_required
def user_articles(request):
    my_articles={}
    if request.user.is_authenticated:
        my_articles = MyArticle.objects.filter(user = request.user)
        return render(request, 'partials/my_articles.html',{"my_articles":my_articles})
    else:
        #l'utilisatrur nest pas authentifier
        return redirect('login_blog')
    

@login_required
def retrait_commission_affillie(request):

    from .forms import FormRetraitAffilie
    messages_error = list()
    if request.method == 'POST':
        try:
            form = FormRetraitAffilie(request.POST, request.FILES)
            if form.is_valid():
                amount = form.cleaned_data["amount"]
                nom_du_beneficaire = form.cleaned_data['nom_du_beneficaire']
                phone_number = form.cleaned_data["phone_number"]
                phone_number_confirmation = form.cleaned_data["phone_number_confirmation"]

                if( amount and nom_du_beneficaire and phone_number and phone_number == phone_number_confirmation):
                    affiliete = MyAffilliates.objects.filter(user = request.user)
                    if(len(affiliete) == 1):
                        affiliete = affiliete[0]
                        amount = int(amount)
                        if amount <= affiliete.solde:
                            # on verifi le phone_number

                            from activation.phone_number import PhoneNumber
                            cleanned_phone_number, is_it_corret = PhoneNumber(phone_number).is_valid_phone_number()

                            if is_it_corret:
                                RetraitAffilie.objects.create(
                                    affiliete = affiliete,
                                    amount = amount,
                                    nom_du_beneficaire = nom_du_beneficaire,
                                    numero_de_retrait = cleanned_phone_number,
                                    status = RetraitAffilie.Status.EN_ATTENTE,
                                    motif_du_gestionnaire = 'En attente de traitement'
                                ).save()
                                return redirect('user_dashboard')


                            else:
                                messages_error.append('LE numero de telephone est incorrect')

                        else:
                            messages_error.append(f'solde insuffusant.Vous ne disposez que de {affiliete.solde} FCFA sur votre compte')
                    elif len(affiliete) == 0:
                        messages_error = 'Vous n\'êtes pas encore affilié. Bien vouloir nous rejoindre notre programme d\'affiliation pour générer des revenus automatiques'

                    else:
                        messages_error = 'Nous avons trouvé plusieurs affiliés avec ce même compte. Bien vouloir joindre le service client.'
                        print('affiliete',affiliete, len(affiliete))
                else:
                    if not amount:
                        messages_error.append("Montant incorrect")
                    elif not nom_du_beneficaire:
            
                        messages_error.append("Le nom du compte MOMO/OM est incorrect ")
                    elif not phone_number:
            
                        messages_error.append("Numéro de téléphone incorrect")
                    elif phone_number != phone_number_confirmation:
                        messages_error.append(f'Les numéro {phone_number} et {phone_number_confirmation} sont differents')
            else:
                messages_error.append('Fomulaire invalide')
            

            return render(request, 'partials/retrait_commission_affillie.html', {"form": form,'messages_error':messages_error})
        except Exception as e:
            print('exception in retrait_commission_affillie jhdjzkk:',str(e))
            messages_error.append("une erreur est survenu durant l'initialisation de votre demande compte")
            return render(request, 'partials/retrait_commission_affillie.html', {"form": form,'messages_error':messages_error})
                                   
    form = FormRetraitAffilie()
    return render( request, 'partials/retrait_commission_affillie.html', {"form": form,"messages_error":messages_error})












