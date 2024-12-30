from django.db import models
from app_auth.models import User
from home.models import MyAffilliates
from .calculate import NOMBRE_DE_MOIS_MAX_AUTORISER_POUR_LA_DEMANDE_DACTIVATION


# Create your models here.

class Activation(models.Model):
    class Statut(models.TextChoices):
        ACTIVEE = 'ACTIVEE'
        ENCOUR = 'ENCOUR'
        EXPIREE = 'EXPIREE'

   
    user= models.ForeignKey(User, on_delete= models.CASCADE, null=True)
    date_de_payement = models.DateTimeField(auto_now_add=True)
    small_date_de_payement = models.DateField(auto_now_add=True)
    who_many_months = models.PositiveSmallIntegerField(default=0)
    is_expirated = models.CharField(
        max_length=10,
        choices=Statut.choices,
        default=Statut.ACTIVEE,
    )
    product_key = models.CharField(primary_key=True,max_length=60, default="")
    #serial_number = models.CharField(max_length=60, default="")
    infos_of_all_installed_pc_with_this_key = models.TextField(default='[]')
    #date_d_debut_d_uitlisation =  models.DateField(auto_now_add=True)
    #ids_of_installed_pc = models.TextField(default="[]" , max_length=255)
    number_of_pc = models.PositiveSmallIntegerField(default=1)
    affilliate = models.ForeignKey(MyAffilliates,on_delete=models.CASCADE, null=True)
    somme_gagner_par_l_affilie   = models.IntegerField(default=0)
    who_many_free_days = models.PositiveSmallIntegerField(default=0)
    is_he_a_new_client_client_for_this_affilliate = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"USER: {self.user} |DATE DE DEBUT: {self.date_de_payement}  |NOMBRE DE MOIS :  {self.who_many_months} | number of pc :{self.number_of_pc}"

""" CASCADE : Supprime tous les objets qui référencent l'objet supprimé.
python

Exécuter

Copier
author = models.ForeignKey(Author, on_delete=models.CASCADE)
PROTECT : Empêche la suppression de l'objet référencé si des objets l'utilisent.
python

Exécuter

Copier
author = models.ForeignKey(Author, on_delete=models.PROTECT)
SET_NULL : Définit la clé étrangère sur NULL lorsque l'objet référencé est supprimé. Cela nécessite que le champ soit nullable.
python

Exécuter

Copier
author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
SET_DEFAULT : Définit la clé étrangère sur sa valeur par défaut lorsque l'objet référencé est supprimé.
python

Exécuter

Copier
author = models.ForeignKey(Author, on_delete=models.SET_DEFAULT, default=1)
DO_NOTHING : Ne fait rien, laisse le développeur gérer la situation.
python

Exécuter

Copier
author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)
Exemple d'uti """

class InitPayementOfLicence(models.Model):
    user= models.ForeignKey(User, on_delete= models.CASCADE, null=True)
    nombre_de_mois = models.PositiveSmallIntegerField(default=1)
    date_of_initialise = models.DateTimeField(auto_now_add=True)
    number_of_pc = models.PositiveSmallIntegerField(default=1)
    promo_code= models.CharField(max_length=60,default='aaaa')
    payement_phone_number = models.PositiveIntegerField(default=674579282)
    operateur_mobile= models.CharField(max_length=60,default='')


    def __str__(self) -> str:
        return f"USER: {self.user} |date_of_initialise: {self.date_of_initialise}  |NOMBRE DE MOIS :  {self.nombre_de_mois}"


