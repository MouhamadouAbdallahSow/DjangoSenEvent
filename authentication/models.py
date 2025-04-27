from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    PROFILE_CHOICES = [
        ("visitor", _("Visiteur")),
        ("creator", _("Créateur")),
        ("participant", _("Participant")),
    ]
    prenom = models.CharField(max_length=64)
    nom = models.CharField(max_length=64)
    profile_type = models.CharField(
        max_length=20,
        choices=PROFILE_CHOICES,
        default="visitor",
    )
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)
    

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def get_full_name(self):
        return f"{self.prenom} {self.nom}"
    
    def is_visitor(self):
        return self.profile_type == "visitor"


    def is_creator(self):
        return self.profile_type == "creator"

    def is_participant(self):
        return self.profile_type == "participant"
