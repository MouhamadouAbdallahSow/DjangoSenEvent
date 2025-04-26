from .models import Inscription, Intervenant, Evenement, Categorie, Avis, LienReseauSociaux
from django.contrib import admin

# Register your models here.
admin.site.register(Inscription)
admin.site.register(Intervenant)
admin.site.register(Evenement)
admin.site.register(Categorie)
admin.site.register(Avis)
