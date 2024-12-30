from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from django.http import JsonResponse
from .forms import GetActivation
from django.contrib.auth.decorators import login_required
from datetime import date
import datetime
from time import time
from math import sqrt
import random
import string
from dateutil.relativedelta import relativedelta
from app_auth.multipleAccountWithUsername import search_the_user, clean_username
from home.models import MyAffilliates
from .models import InitPayementOfLicence,Activation 

from .encript_decrypt import encrypt_data,decrypt_data
from .calculate import Montant_mensuel_de_la_license , NOMBRE_DE_MOIS_MAX_AUTORISER_POUR_LA_DEMANDE_DACTIVATION, NOMBRE_MAX_DE_PC_POUR_UNE_MEME_CLE_PRODUIT, TAUX_DE_RENTABILITE_DE_L_AFFILIE
# Create your views here.

def activation_index(request):

    return render(request,'activation/activation_index.html')


@login_required
def get_activation(request):
    do_i_ask_affillite_code = True if try_to_get_affillite_code_if_exist(request.user) is None else False
    messages_error=[]  
    duration_valid=""
    my_affilliates_first_infos = list()

    if do_i_ask_affillite_code:
        my_affilliates = MyAffilliates.objects.all()
        for my_affilliate in my_affilliates:
            my_affilliates_first_infos.append([my_affilliate.code_affillie, my_affilliate.number_of_free_days])
            print('my_affilliate:', my_affilliate.code_affillie, my_affilliate.number_of_free_days)
        
    print('my_affilliates_first_infos:', my_affilliates_first_infos)

    if not  request.user.is_authenticated:
        print("The user isn't authenticate", request.user )

        #return redirect("login_blog")


    if request.method=="POST" :
        try:
            form=GetActivation(request.POST)
            if form.is_valid():
                durree =form.cleaned_data['duration']
                number_of_pc =form.cleaned_data['number_of_pc']
                payement_phone_number =form.cleaned_data['payement_phone_number']
                code_affillie = try_to_get_affillite_code_if_exist(request.user) 
                code_affillie = code_affillie if code_affillie is not None else form.cleaned_data['code_affillie']
                print('code_affillie:',code_affillie)
                print('zzzzzzzzzzzz payement_phone_number:',payement_phone_number)

                if payement_phone_number is not None:
                    from .phone_number import PhoneNumber
                    print('ddddddddddddd payement_phone_numcccber:',payement_phone_number)
                    
                    (payement_phone_number, is_it_correct_phonee_number) = PhoneNumber(payement_phone_number).is_valid_phone_number()
                    print('ccccccc payement_phone_numcccber:',payement_phone_number)
                    if not is_it_correct_phonee_number:
                        
                        messages_error.append("Le numero de telephone est incorect")
                        print('user',request.user)

                        return render(request,'activation/get_activation.html.',{"form":form,"my_affilliates_first_infos":my_affilliates_first_infos,'do_i_ask_affillite_code':do_i_ask_affillite_code, "Montant_mensuel_de_la_license":Montant_mensuel_de_la_license,"messages_error":messages_error})
            
                print('aaaaaaaaa payement_phone_number:',payement_phone_number)
                
                if (request.user is not None )and (durree is not None) and (number_of_pc is not None)and (payement_phone_number is not None):
                    print(request.user)
                    print('bbbbbbbbbbb payement_phone_number:',payement_phone_number)
                    data = {
                        'NDM' : durree,
                        'code_affillie':code_affillie,
                        'number_of_pc':number_of_pc,
                        'payement_phone_number':payement_phone_number,
                    } 

                    donnees_criptees = str(encrypt_data(data=data)) 
                    print(donnees_criptees,type(donnees_criptees))
                    #return redirect(f'/activation/confirme_quote_before_init_payement?NDM={durree}&code_affillie={code_affillie}&number_of_pc={number_of_pc}&payement_phone_number={payement_phone_number}')
                    return redirect(f'/activation/confirme_quote_before_init_payement?q={donnees_criptees}')
                    #return redirect('confirme_quote_before_init_payement')
                    #return render(request,'partials/user_dashboard.html')
                else:
                    messages_error.append("Une erreur est survenue sur le formulaire")
                    print('user',request.user)
                    print('durree',durree)

                    return render(request,'activation/get_activation.html.',{"form":form,"my_affilliates_first_infos":my_affilliates_first_infos,'do_i_ask_affillite_code':do_i_ask_affillite_code, "Montant_mensuel_de_la_license":Montant_mensuel_de_la_license,"messages_error":messages_error})
            else:
                
                for field in form.errors:
                        form[field].field.widget.attrs['class'] += ' is-invalid'

                messages_error.append("Le formulaire est invalide")
                if request.POST['duration'] > NOMBRE_DE_MOIS_MAX_AUTORISER_POUR_LA_DEMANDE_DACTIVATION :
                    messages_error.append(f"Le nombre maximal de mois autorisé est de {NOMBRE_DE_MOIS_MAX_AUTORISER_POUR_LA_DEMANDE_DACTIVATION} mois")
                    print("eeeeeeeeeeeeee")
                else :
                    print("request.POST['duration'] :",request.POST['duration'] )
                if len(request.POST['duration'])==0:
                    form[0].field.widget.attrs['class'] += ' is-invalid'

                    duration_valid="Veuillez remplir ce champ"

                return render(request,'activation/get_activation.html',{"form":form,"my_affilliates_first_infos":my_affilliates_first_infos,'do_i_ask_affillite_code':do_i_ask_affillite_code,"Montant_mensuel_de_la_license":Montant_mensuel_de_la_license,"messages_error":messages_error,'duration_valid':duration_valid})
        except:
            messages.error(request,"ERREUR D'AUTHENTIFICATION")
            
            form=GetActivation(request.GET)
            return render(request,'activation/get_activation.html',{"form":form,"my_affilliates_first_infos":my_affilliates_first_infos,'do_i_ask_affillite_code':do_i_ask_affillite_code,"Montant_mensuel_de_la_license":Montant_mensuel_de_la_license})

    else:
        form=GetActivation(request.GET)
        return render(request,'activation/get_activation.html',{"form":form,"my_affilliates_first_infos":my_affilliates_first_infos,'do_i_ask_affillite_code':do_i_ask_affillite_code,"Montant_mensuel_de_la_license":Montant_mensuel_de_la_license})
    
    
    return render(request,'activation/get_activation.html',{"form":form,"my_affilliates_first_infos":my_affilliates_first_infos,'do_i_ask_affillite_code':do_i_ask_affillite_code,"Montant_mensuel_de_la_license":Montant_mensuel_de_la_license})

@login_required
def confirme_quote_before_init_payement(request):
    try: 
        donnees_cryptees = request.GET['q']
        data = decrypt_data(donnees_cryptees)
        
        nombre_de_mois =  data['NDM']
        code_affillie =  data['code_affillie']
        number_of_pc =  data['number_of_pc']
        payement_phone_number =  data['payement_phone_number']
        number_of_free_days = 0
    
        print('nombre_de_mois:',nombre_de_mois)
        
        promotion_code = MyAffilliates.objects.filter(code_affillie = code_affillie).first()
       
        number_of_free_days = 0 if promotion_code is None else promotion_code.number_of_free_days

       

        print('confirme_quote_before_init_payement number_of_free_days',number_of_free_days)
        try:
            nombre_de_mois = int(nombre_de_mois)
            number_of_pc = int(number_of_pc)

            if number_of_pc > NOMBRE_MAX_DE_PC_POUR_UNE_MEME_CLE_PRODUIT :
                raise ValueError('Le nombre de pc a dépassé la limite permise')
            if nombre_de_mois > NOMBRE_DE_MOIS_MAX_AUTORISER_POUR_LA_DEMANDE_DACTIVATION :
                raise ValueError('Le nombre de mois est superieur au max autorisé')

            from .phone_number import PhoneNumber
            payement_phone_number, is_it_correct_phonee_number = PhoneNumber(payement_phone_number).is_valid_phone_number()
            if not is_it_correct_phonee_number :
                raise ValueError('Le numero de payement est incorrect')
            operateur_mobile = None
            if PhoneNumber(payement_phone_number).is_it_mnt_number(payement_phone_number):
                operateur_mobile = 'MTN'
            elif PhoneNumber(payement_phone_number).is_it_orange_number(payement_phone_number):
                operateur_mobile = 'ORANGE'
            else:
                raise ValueError("Erreur: l'operateur téléphonique lié à ce nulero n'a pu etre identifié")


            payement = InitPayementOfLicence(user = request.user, nombre_de_mois =nombre_de_mois,number_of_pc =number_of_pc, promo_code = code_affillie,payement_phone_number = payement_phone_number, operateur_mobile= operateur_mobile )
            payement.save()
            return render(request, "activation/confirme_quote_before_init_payement.html",{'nombre_de_mois':nombre_de_mois, 'number_of_free_days':number_of_free_days,'Montant_mensuel_de_la_license':Montant_mensuel_de_la_license, 'number_of_pc':number_of_pc, 'total_amount':nombre_de_mois*Montant_mensuel_de_la_license*number_of_pc,'payement_phone_number':payement_phone_number})
        except Exception as e  :
            print("qqqqq",e)
            form=GetActivation(request.GET)
            return render(request,'activation/get_activation.html',{"form":form,"Montant_mensuel_de_la_license":Montant_mensuel_de_la_license,"number_of_pc":number_of_pc})

    except Exception as e  :
        print("dddddd", e)
        form=GetActivation(request.GET)
        return render(request,'activation/get_activation.html',{"form":form,"Montant_mensuel_de_la_license":Montant_mensuel_de_la_license,})
    
    return render(request,'activation/get_activation.html',{"form":form,"Montant_mensuel_de_la_license":Montant_mensuel_de_la_license,})




@login_required
def init_payement(request):
    #recuper le nombre de mois
    data = InitPayementOfLicence.objects.filter(user = request.user).last()
    print(data)
    nombre_de_mois = data.nombre_de_mois
    number_of_pc = data.number_of_pc
    total_amount = nombre_de_mois * Montant_mensuel_de_la_license*number_of_pc
    promo_code = data.promo_code







    from pymesomb.operations import PaymentOperation
    from pymesomb.utils import RandomGenerator
    from datetime import datetime
    try:
        operation = PaymentOperation('2e4de0586e2689e6cd5a1cf152ca19ecf4302b9c', '962085e2-5f3e-460b-b0ec-d9c007722b4c', 'eb52d60b-3265-4f83-a7ee-e888eff3a3b8')
        response = operation.make_collect({
            'amount': total_amount,
            'service': data.operateur_mobile,
            'payer': str(data.payement_phone_number),
            'date': datetime.now(),
            'nonce': RandomGenerator.nonce(),
            'trxID': str(data.id)
        })
        print(response.is_operation_success())
        print(response.is_transaction_success())
        assert(response.is_operation_success() == True and response.is_transaction_success() ==True)
        
    
    except Exception as e:
        print("init_payement djkabdjkza   , exception",e)

        return render(request, 'activation/licence pay failled.html',{'nombre_de_mois':nombre_de_mois,'Montant_mensuel_de_la_license':Montant_mensuel_de_la_license,'total_amount':total_amount,'number_of_pc':number_of_pc,'payement_phone_number':data.payement_phone_number,})


    else:

        affilliate = MyAffilliates.objects.filter(code_affillie = promo_code).first()
        if affilliate is not None:
            somme_gagner_par_l_affilie = total_amount * TAUX_DE_RENTABILITE_DE_L_AFFILIE
            if is_it_the_first_activation_of_this_user(request.user):
                somme_gagner_par_l_affilie -= int((affilliate.number_of_free_days/30)*Montant_mensuel_de_la_license*number_of_pc)
            affilliate.solde += somme_gagner_par_l_affilie
            affilliate.save()
            is_he_a_new_client_client_for_this_affilliate = True if len(Activation.objects.filter(user = request.user, affilliate = affilliate)) ==0 else False 
        else:
            somme_gagner_par_l_affilie = 0
            is_he_a_new_client_client_for_this_affilliate = False

        activation =Activation(user = request.user,
                                who_many_months = nombre_de_mois,
                                is_expirated=Activation.Statut.ACTIVEE,
                                product_key= generate_random_key(),
                                affilliate = affilliate,
                                who_many_free_days = affilliate.number_of_free_days,
                                somme_gagner_par_l_affilie = somme_gagner_par_l_affilie,
                                number_of_pc =number_of_pc,
                                is_he_a_new_client_client_for_this_affilliate =is_he_a_new_client_client_for_this_affilliate 
                                )
        activation.save()




        return render(request, 'activation/licence pay succesfully.html',{'nombre_de_mois':nombre_de_mois,'Montant_mensuel_de_la_license':Montant_mensuel_de_la_license,'total_amount':total_amount,'product_key':activation.product_key,'number_of_pc':number_of_pc,})


    
def check_ativation(request):
    from django.core.cache import cache
    from .calculate import SOFT_KEY
    try:
        donnees_decryptees = decrypt_data(request.GET["q"],KEY=SOFT_KEY)
        
        print('donnees_decryptees 515:',donnees_decryptees)
        product_key = donnees_decryptees["product_key"]
        serial_number = donnees_decryptees["serial_number"]
        id_of_pc = donnees_decryptees["id_of_pc"]
        date_time = donnees_decryptees["current_date"]
        type_of_activation= donnees_decryptees['type_of_activation']
        print("id_of_pc:",id_of_pc)
        
    except Exception as e:
        print("check_ativation",e)
        print("requette invalide")

    else:
        try:
            if type_of_activation == 'start for free':
                pass




            his_activation = Activation.objects.get(product_key = product_key)
            if his_activation:
                actual_infos = eval(his_activation.infos_of_all_installed_pc_with_this_key)
                print('actual_infos:',actual_infos, type(actual_infos))
                ids_of_installed_pc =  [infos['id_of_installed_pc'] for infos in actual_infos if 'id_of_installed_pc' in infos.keys()]
                print('ids_of_installed_pc:',ids_of_installed_pc)
                try:
                    print('actual_infos',actual_infos)
                    if len(actual_infos) < his_activation.number_of_pc :
                        new_infos = {
                            'id_of_installed_pc':str(id_of_pc) + " Fast Sofware",
                            'date_d_debut_d_uitlisation':date.today(),
                            'serial_number': serial_number,
                        }
                        actual_infos.append(new_infos)
                        his_activation.infos_of_all_installed_pc_with_this_key = str(actual_infos)
                        
                        # Création de données manuelles
                        nombre_de_jour_restant,nombre_de_jours_reduit = calculer_le_nombre_de_jour_restantet_reduitice(his_activation.small_date_de_payement,his_activation.who_many_months) 
                        nombre_de_jour_restant +=  his_activation.who_many_free_days
                        data =  { 
                            'nombre_de_jours_restant': nombre_de_jour_restant,
                            'nombre_de_jours_reduit': nombre_de_jours_reduit,
                            "succes_message":f"Félécitation votre clé produit a été activée avec succèss.\n Vous bénéficiez de {nombre_de_jour_restant} supplémentaires",
                            'ok_status': encriptation(str(date_time)),
                                }
                        his_activation.save()
                        
                        
                        return JsonResponse({'q':encrypt_data(data,KEY=SOFT_KEY) }, safe=False)

                    else:
                        print("ids_of_installed_pc:",ids_of_installed_pc)
                
                        data =  {
                            'nombre_de_jours_restant':None,
                            'nombre_de_jours_reduit': None,
                            'error_message': f'Le nombre de machine définit pour cette clé est déjà atteint.\nElle a été achétée pour {his_activation.number_of_pc} pc.\n Veuillez acheter une autre',
                            'ok_status': encriptation(str(date_time)),
                            }
                except :
                    data =  {
                            'nombre_de_jours_restant':None,
                            'nombre_de_jours_reduit': None,
                            'error_message': "Une erreur est survenue l'hors de la validation de votre clé",
                            'ok_status': encriptation(str(date_time)),
                            }
                    
                finally:
                    return JsonResponse({'q':encrypt_data(data,KEY=SOFT_KEY) }, safe=False)
                # Retourner les données personnalisées en JSON
                return JsonResponse({'q':encrypt_data(data,KEY=SOFT_KEY) }, safe=False)
        except :
            
            
            data =  {

                     'nombre_de_jours_restant':None,
                            'nombre_de_jours_reduit': None,
                    'error_message': 'Votre clé produit n\'a pas été trouvée',
                    'ok_status': encriptation(str(date_time)),
                     }
            return JsonResponse({'q':encrypt_data(data,KEY=SOFT_KEY) }, safe=False)




def encriptation(s: str) -> str:
    value = ""
    for char in s:
        value += str(int(sqrt(ord(char) ))* (s.index(char) + 1) ) # Poids basé sur la position
        #print(value,"  ",char)
    return value

""" 
def second_encriptation(s: str) -> str:
    value = 1
    for char in s:
        value *= int(int(sqrt(ord(char) ))* (s.index(char) + 1) ) # Poids basé sur la position
        print(value,"  ",char)
    return value
 """


def generate_random_key(length=11):
    """Génère une clé aléatoire basée sur le timestamp."""
    # Obtenir le timestamp actuel
    timestamp = int(time()*1000)

    # Générer une partie aléatoire
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    random_part = random_part.upper()
    # Combiner le timestamp et la partie aléatoire
    key = f"{timestamp}{random_part}"
    final_key = ''
    for i,char in enumerate (key):
        final_key += char
        if (i+1)%4 ==0 and i!=0 and i!= len(key)-1:
            final_key += '-'
        #print("final_key:",final_key,i)

    return final_key


def calculer_le_nombre_de_jour_restantet_reduitice(payement_date, nombre_de_mois):


    # Calcul de la différence
    if date.today() < payement_date:
        return None,None
    delta = relativedelta(date.today(), payement_date)
    print("delta:",delta)

    # Calculer le nombre total de jours
    total_days_to_reduice = delta.years * 365 + delta.months * 30 + delta.days
    print("total_days_to_reduice:",total_days_to_reduice)
    total_days = max (nombre_de_mois*30 - total_days_to_reduice,0)
    print('calculer_le_nombre_de_jour_restantet_reduitice(start_date, nombre_de_mois):total_days: ',total_days)
    return max(0,total_days),total_days_to_reduice
    
def try_to_get_affillite_code_if_exist(user):
    try:
        latest_activation = Activation.objects.filter(user = user).latest('date_de_payement')
        print('latest_activation.affilliate', latest_activation.affilliate)
        if latest_activation.affilliate is not None:
            code_affillie = latest_activation.affilliate.code_affillie
            print('latest_activation.affilliate.code_affillie', code_affillie)
            return code_affillie
    except Exception as e:
        print("try_to_get_affilliet_code_if_exist()",e)
        return None
    
def is_it_the_first_activation_of_this_user(user):
    if len(Activation.objects.filter(user = user)) == 0:
        return  True
    return False
