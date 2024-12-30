from django.contrib import admin
from .models import RetraitAffilie
from django.utils.html import format_html

class RetraitAffilieAdmin(admin.ModelAdmin):
    # Liste des champs qui seront affichés dans la liste
    list_display = ('affiliete', 'status_colored', 'amount', 'numero_de_retrait',
                    'nom_du_beneficaire', 'date_de_demmande',
                    'date_de_traitement',  # Modification ici
                    'motif_du_gestionnaire')
    
    # Champs qui peuvent être modifiés dans le formulaire
    fields = ('date_de_traitement', 'status', 'motif_du_gestionnaire')  # Champs éditables
    readonly_fields = ('affiliete', 'amount', 'numero_de_retrait',
                       'date_de_demmande', 'nom_du_beneficaire')  # Champs non éditables

    # Optionnel : pour filtrer et rechercher
    search_fields = ('status', 'date_de_demmande')
    list_filter = ('status', 'date_de_demmande')

    def save_model(self, request, obj, form, change):
        if change:
            affiliate = obj.affiliete
            if (affiliate is not None) and obj.status == obj.Status.PAYE:
                affiliate.solde -= obj.amount
                affiliate.save()

        super().save_model(request, obj, form, change)

    def status_colored(self, obj):
        # Changez la couleur en fonction d'une variable du modèle
        if obj.status == "PAYE":    
            couleur = 'green'
        elif obj.status == 'EN ATTENTE':
            couleur = 'orange'
        elif obj.status == 'ECHEC' or obj.status == 'REFUSE':
            couleur = 'red'
        else:
            couleur = 'blue'

        return format_html('<span style="background-color: {};">{}</span>', couleur, obj.status)  # Modification ici

    status_colored.short_description = 'Status'

# Enregistrement du modèle et de l'administration
admin.site.register(RetraitAffilie, RetraitAffilieAdmin)