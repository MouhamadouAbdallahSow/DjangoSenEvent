from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required
def user_profile(request):
    """Affiche la page de profil avec le style adapté"""
    user = request.user
    
    # Ajouter des données supplémentaires selon le type de profil
    context = {
        'user': user,
        'MEDIA_URL': settings.MEDIA_URL  # Pour accéder à l'URL des médias dans le template
    }
    
    return render(request, 'profiles/user_profile.html', context)