from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from events.models import Evenement, Intervenant, LienReseauSociaux, validate_video_file, validate_image_file, TypeTicket
from .region_ville import REGIONS_VILLES

# Taille maximale des fichiers en octets (10 Mo pour images, 50 Mo pour vidéos)
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 50 MB
##
def ville_par_region(request):
    region = request.GET.get('region', None)
    if region and region in REGIONS_VILLES:
        villes = REGIONS_VILLES[region]
        return JsonResponse({'villes': villes}, status=200)
    return JsonResponse({'error': 'Région invalide'}, status=400)


def Editer(request):
    if request.method == 'POST':
        # Récupérer les données principales de l'événement
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        slogan = request.POST.get('slogan')
        lien_diffusion = request.POST.get('lien')
        date = request.POST.get('date')
        heure_debut = request.POST.get('heure')
        chronogramme = request.FILES.get('chronogramme')
        region = request.POST.get('region')
        ville = request.POST.get('ville')
        lieu_exact = request.POST.get('Lieu_exact')

        # Validation des données principales
        if not titre or not description or not date or not heure_debut or not region or not ville:
            return render(
                request,
                'CreateEvent/edite.html',
                {'error': 'Tous les champs obligatoires doivent être remplis.'}
            )
        
        # Créer l'événement
        evenement = Evenement.objects.create(
            titre=titre,
            description=description,
            lieu=f"{region} / {ville} / {lieu_exact}",
            slogan=slogan,
            lien_diffusion=lien_diffusion,
            date=date,
            heure=heure_debut,
            createur=request.user.createur,
            video=None,
            image=None,
        )
        request.session['evenement_id'] = evenement.id

        # Traiter les intervenants
        i = 0
        while True:
            # Récupérer les données de l'intervenant
            prenom = request.POST.get(f"speakers[{i}][prenom]")
            if not prenom:
                break

            nom = request.POST.get(f"speakers[{i}][nom]")
            fonction = request.POST.get(f"speakers[{i}][fonction]")
            description_fonction = request.POST.get(f"speakers[{i}][description]")
            photo = request.FILES.get(f"speakers[{i}][photo]")
            instagram = request.POST.get(f"speakers[{i}][instagram]")
            facebook = request.POST.get(f"speakers[{i}][facebook]")
            twitter = request.POST.get(f"speakers[{i}][twitter]")
            linkedin = request.POST.get(f"speakers[{i}][linkedin]")

            # Créer l'intervenant
            intervenant = Intervenant.objects.create(
                nom=f"{prenom} {nom}",
                fonction=fonction,
                description_fonction=description_fonction,
                photo_profil=photo if photo else None,
                
            )
            intervenant.evenement.add(evenement)

            LienReseauSociaux.objects.create(
                utilisateur=intervenant,
                instagram=instagram,
                facebook=facebook,
                twitter=twitter,
                linkedIn=linkedin,
            )

            i += 1

        return redirect('AddEvent:Banniere')

    return render(request, 'CreateEvent/edite.html')


def Multimedia(request):
    if request.method == 'POST':
        typeFichier = request.POST.get('mediaType')
        image = request.FILES.get('ImageInput')
        video = request.FILES.get('videoInput')
        print(image)
        if (not image) and (not video):
            return render(
                request,
                'CreateEvent/Banniere.html',
                {'error': 'Veuillez ajouter une image ou une vidéo.'}
            )

        evenement_id = request.session.get('evenement_id')
        if not evenement_id:
            messages.error(request, "Session expirée. Veuillez recommencer l'inscription.")
            return redirect('AddEvent:Editer')

        try:
            evenement = Evenement.objects.get(id=evenement_id)
        except Evenement.DoesNotExist:
            messages.error(request, "L'événement spécifié est introuvable.")

        if typeFichier == 'image' and image:
            if validate_image_file(image):
                return render(request, 'CreateEvent/Banniere.html', {'error': 'Format d’image invalide.'})
            if image.size > MAX_IMAGE_SIZE:
                return render(request, 'CreateEvent/Banniere.html', {'error': 'L’image dépasse la taille maximale de 10 Mo.'})
            evenement.image = image

        elif typeFichier == 'video' and video:
            if validate_video_file:
                return render(request, 'CreateEvent/Banniere.html', {'error': 'Format de vidéo invalide.'})
            if video.size > MAX_VIDEO_SIZE:
                return render(request, 'CreateEvent/Banniere.html', {'error': 'La vidéo dépasse la taille maximale de 50 Mo.'})
            evenement.video = video

        else:
            return render(request, 'CreateEvent/Banniere.html', {'error': 'Choisissez un type de fichier valide.'})

        evenement.save()
        return redirect('AddEvent:ticketGestion')

    return render(request, 'CreateEvent/Banniere.html')


def Ticket(request):
    if request.method == 'POST':
        type_evenement =  request.POST.get('evenType')
        evenement_id = request.session.get('evenement_id')
        if not evenement_id:
            messages.error(request, "Session expirée. Veuillez recommencer l'inscription.")
            return redirect('AddEvent:Editer')

        try:
            evenement = Evenement.objects.get(id=evenement_id)
        except Evenement.DoesNotExist:
            messages.error(request, "L'événement spécifié est introuvable.")
            return redirect('AddEvent:Editer')
        if type_evenement:
            typeticket = TypeTicket.objects.create(
                type = type_evenement
            )
            if type_evenement == 'payant':
                nom_ticket = request.POST.get('ticketName')
                prix_ticket = request.POST.get('ticketPrice')
                typeticket.nom =nom_ticket
                typeticket.prix =prix_ticket
            evenement.ticket = typeticket
            evenement.save()
        else:
            return render(request, 'CreateEvent/ticket.html',{'error': "Type d'evenement invalide."})
        
        return redirect('AddEvent:Reviser')
    return render(request, 'CreateEvent/ticket.html')


def Reviser(request):
    evenement_id = request.session.get('evenement_id')
    if not evenement_id:
        messages.error(request, "Session expirée ou événement introuvable.")
        return redirect('AddEvent:Editer')
    
    try:
        evenement = Evenement.objects.get(id=evenement_id)
    except Evenement.DoesNotExist:
        messages.error(request, "L'événement spécifié est introuvable.")
        return redirect('AddEvent:Editer')
    return render(request, 'CreateEvent/Reviser.html', {'evenement':evenement})
