from django.db import models
from app_auth.models import User
from activation.models import InitPayementOfLicence
from datetime import date
from home.models import MyAffilliates

# Create your models here.

class RetraitAffilie(models.Model):
    class Status(models.TextChoices):
        EN_ATTENTE = 'EN ATTENTE'
        PAYE = 'PAYE',
        ECHEC = 'ECHEC',
        REFUSE = 'REFUSE',
    affiliete = models.ForeignKey(MyAffilliates, on_delete=models.CASCADE, null=False)
    amount = models.PositiveIntegerField(null=False )
    numero_de_retrait = models.PositiveIntegerField(null=False)
    nom_du_beneficaire = models.CharField(default='VIDAL PAVER TSAFACK NANA', max_length=255)
    date_de_demmande = models.DateTimeField(auto_now_add=True)
    date_de_traitement = models.DateTimeField(null=True)
    status = models.CharField(choices=Status.choices,default= Status.EN_ATTENTE, max_length=30)
    motif_du_gestionnaire = models.TextField(max_length=255,default='')


    def __str__(self):
        return f'{self.status}|{self.date_de_demmande}|{self.amount}'









