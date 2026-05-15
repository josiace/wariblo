from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from .models import User


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    role = request.GET.get('role', 'influencer')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Votre compte a été créé avec succès!')
            return redirect('dashboard')
    else:
        initial_data = {'role': role}
        form = RegistrationForm(initial=initial_data)
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    messages.success(request, 'Connexion réussie!')
                    return redirect('dashboard')
            except User.DoesNotExist:
                messages.error(request, 'Email ou mot de passe incorrect.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté.')
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user
    if user.is_influencer:
        return redirect('influencer_dashboard')
    elif user.is_advertiser:
        return redirect('advertiser_dashboard')
    else:
        return redirect('admin:index')

