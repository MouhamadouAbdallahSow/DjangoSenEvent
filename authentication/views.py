from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignupForm, ProfileChoiceForm
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.forms import SetPasswordForm



User = get_user_model()

# Inscription (pas de compte)
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.prenom = form.cleaned_data["prenom"]
            user.nom = form.cleaned_data["nom"]
            user.save()
            
            # Spécifier manuellement le backend d'authentification
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            
            login(request, user)
            messages.success(request, "Inscription réussie !")
            return redirect("authentication:choose_profile")
    else:
        form = SignupForm()
    return render(request, "authentication/signup.html", {"form": form})


# Choix du type d'utilisateur (createur , visiteur, participant)
@login_required
def choose_profile_view(request):
    if request.method == 'POST':
        form = ProfileChoiceForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profiles:user_profile")  # Redirection après choix du profil
    else:
        form = ProfileChoiceForm()
    return render(request, 'authentication/choose_profile.html', {'form': form})

# Se connecter (possede un compte)
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("profiles:user_profile")  # Redirection vers la page unique
        else:
            error_message = "Invalid username or password."
    else:
        error_message = None
    
    return render(request, "authentication/login.html", {"error_message": error_message})

def logout_view(request):
    logout(request)
    return redirect('home:acceuil')  # Redirige vers la page d'accueil

def set_password_view(request):
    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Ajouter cette ligne cruciale
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            
            if 'force_password_setup' in request.session:
                del request.session['force_password_setup']
                request.session.modified = True
            
            login(request, user)  # Maintenant le backend est défini
            return redirect('profiles:user_profile')
    else:
        form = SetPasswordForm(request.user)
    return render(request, 'authentication/set_password.html', {'form': form})