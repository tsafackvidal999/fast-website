from django import forms

class  FormRetraitAffilie(forms.Form):
    
    from activation.calculate import SOMME_MINIMALE_POUR_DE_L_AFFILIE
    amount = forms.IntegerField(label='Montant',min_value=SOMME_MINIMALE_POUR_DE_L_AFFILIE)
    phone_number = forms.IntegerField (label='Numero MOMO ou OM', min_value=650000000, max_value=699999999)
    phone_number_confirmation = forms.IntegerField(label='Confirmez le numero',min_value=650000000)
    nom_du_beneficaire = forms.CharField(label='Nom du compte MOMO/OM', max_length=255)
