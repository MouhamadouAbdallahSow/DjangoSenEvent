from . import views
from django.urls import path

app_name = 'AddEvent'
urlpatterns = [
    path('api/villes/', views.ville_par_region, name='villes_par_region'),
    path('Editer/', views.Editer, name='Editer'),
    path('Banniere/', views.Multimedia, name='Banniere'),
    path('Type/', views.Ticket, name='ticketGestion'),
    path('Reviser/', views.Reviser, name='Reviser'),
]