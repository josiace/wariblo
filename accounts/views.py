from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_backends
from django.shortcuts import redirect, render

from .forms import LoginForm, RegistrationForm


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    role = request.GET.get("role", "influencer")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Spécifier le backend d'authentification
            backend = get_backends()[0]
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
            login(request, user)
            messages.success(request, "Votre compte a été créé avec succès!")
            return redirect("dashboard")
    else:
        form = RegistrationForm(initial={"role": role})

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Connexion réussie!")
                return redirect("dashboard")
            messages.error(request, "Email ou mot de passe incorrect.")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté.")
    return redirect("login")


@login_required
def dashboard(request):
    user = request.user
    if user.is_influencer:
        return redirect("influencer_dashboard")
    if user.is_advertiser:
        return redirect("advertiser_dashboard")
    return redirect("admin:index")
