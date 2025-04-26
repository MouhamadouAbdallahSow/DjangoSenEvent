from django.db import models
from django.core.exceptions import ValidationError
# from django.contrib.auth.models import User
from authentication.models import CustomUser
from django.conf import settings


from django.core.exceptions import ValidationError

def validate_video_file(value):
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    if not any(value.name.endswith(ext) for ext in video_extensions):
        raise ValidationError("Invalid video format. Allowed formats: .mp4, .avi, .mov, .mkv")

def validate_image_file(value):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    if not any(value.name.lower().endswith(ext) for ext in image_extensions):
        raise ValidationError("Invalid image format. Allowed formats: .jpg, .jpeg, .png, .gif")

class TypeTicket(models.Model):
    type = models.CharField(max_length=100)
    nom = models.CharField(max_length=240, null=True, blank=True)
    prix = models.CharField(max_length=240, null=True, blank=True)

class Evenement(models.Model):
    titre = models.CharField(max_length=240)
    description = models.TextField()
    lieu = models.CharField(max_length=240)
    chronogramme = models.FileField(upload_to='documents/', null=True)
    image = models.ImageField(upload_to='EventImage/')
    slogan = models.CharField(max_length=240, null=True)
    lien_diffusion = models.CharField(max_length=240, null=True)
    video = models.FileField(upload_to='videos/', validators=[validate_video_file], null=True, blank=True)
    date = models.DateField()
    heure = models.TimeField()
    createur = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        related_name='evenements',
        limit_choices_to={'profile_type': 'creator'},
        verbose_name="Créateur",
    )
    ticket = models.ForeignKey(
        TypeTicket, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name='type_ticket'
    )

    def __str__(self):
        return self.titre

    
class Categorie(models.Model): 
    nom = models.CharField(max_length=50, unique=True)
    evenement = models.ManyToManyField(Evenement)
    def __str__(self):
        return self.nom
    

class Inscription(models.Model):
    class Statut(models.TextChoices):
        EN_ATTENTE = 'En attente', 'En attente'
        VALIDE = 'Validée', 'Validée'
        ANNULEE = 'Annulée', 'Annulée'
    date_inscription = models.DateField() 
    statut = models.CharField(
        max_length=20, 
        choices=Statut.choices, 
        default=Statut.EN_ATTENTE  # Le statut par défaut est 'En attente'
    )
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT,  # Si l'utilisateur est supprimé, l'inscription n'est pas supprimée
        related_name='inscriptions'
    )
    evenement = models.ForeignKey(
        Evenement, 
        on_delete=models.PROTECT,
        related_name='inscriptions'
    )

    def __str__(self):
        return f"Inscription de {self.utilisateur.username} pour l'événement {self.evenement.titre} ({self.statut})"

    
class Intervenant(models.Model):
    nom = models.CharField(max_length=240)
    fonction = models.CharField(max_length=240, null=True)
    description_fonction = models.TextField(null=True)
    photo_profil = models.ImageField(upload_to='IntervenantImage/', null=True)
    evenement = models.ManyToManyField(Evenement)
    
    def __str__(self):
        return f"{self.nom}"
    
class LienReseauSociaux(models.Model):
    instagram = models.CharField(max_length=240, null=True, blank=True)
    facebook = models.CharField(max_length=240, null=True, blank=True)
    twitter = models.CharField(max_length=240, null=True, blank=True)
    linkedIn = models.CharField(max_length=240, null=True, blank=True)
    utilisateur = models.OneToOneField(Intervenant, on_delete=models.CASCADE, related_name='Lien_Reseaux')
    
    def __str__(self):
        return f" Les liens reseaux sociaux de {self.utilisateur.nom}"

class Avis(models.Model):
    commentaire = models.TextField()
    evaluation = models.IntegerField(blank=False, null=True)
    date = models.DateField(auto_now_add=True, blank=True)
    utilisateur = models.ForeignKey(
    settings.AUTH_USER_MODEL,  # Remplacez User par settings.AUTH_USER_MODEL
    on_delete=models.PROTECT,
    related_name='Avis'
)

    evenement = models.ForeignKey(Evenement, on_delete= models.PROTECT, related_name='Avis')

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(evaluation__gte=1) & models.Q(evaluation__lte=5),
                name="avis_evaluation_between_1_and_5",
            )
        ]

    def __str__(self):
        return f"Avis de {self.utilisateur.username} (Évaluation: {self.evaluation})"