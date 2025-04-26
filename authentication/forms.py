from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    prenom = forms.CharField(
        max_length=64,
        required=True,
        label="Prénom",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Votre prénom"}),
    )
    nom = forms.CharField(
        max_length=64,
        required=True,
        label="Nom",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Votre nom"}),
    )
    
    # Ajouter ces deux champs explicitement
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre mot de passe'
        })
    )
    
    password2 = forms.CharField(
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmez votre mot de passe'
        })
    )

    class Meta:
        model = CustomUser
        fields = ["prenom", "nom", "email", "username", "password1", "password2"]
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control", 
                "placeholder": "Votre email"
            }),
            "username": forms.TextInput(attrs={
                "class": "form-control", 
                "placeholder": "Votre nom d'utilisateur"
            }),
        }


class ProfileChoiceForm(forms.ModelForm):
    PROFILE_CHOICES_WITH_DESCRIPTIONS = [
        ("visitor", "Visiteur - Accès gratuit aux événements publics"),
        ("creator", "Créateur - Publiez vos propres événements (Payant)"),
        ("participant", "Participant - Rejoignez des événements privés"),
    ]
    
    profile_type = forms.ChoiceField(
        choices=PROFILE_CHOICES_WITH_DESCRIPTIONS,
        required=True,
        label="Type de profil",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = CustomUser
        fields = ['profile_type', 'profile_photo', 'cover_photo']
        widgets = {
            'profile_photo': forms.FileInput(attrs={"class": "form-control"}),
            'cover_photo': forms.FileInput(attrs={"class": "form-control"}),
        }


