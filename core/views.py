from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from .forms import ContactForm
from influencers.models import InfluencerProfile
from advertisers.models import AdvertiserProfile


@cache_page(60 * 15)  # Cache 15 minutes
def landing_page(request):
    return render(request, 'core/landing.html')


def home(request):
    """
    Page d'accueil qui change selon le rôle de l'utilisateur:
    - Non connecté: landing page
    - Annonceur: liste des influenceurs
    - Influenceur: liste des annonceurs
    """
    if not request.user.is_authenticated:
        return render(request, 'core/landing.html')
    
    if request.user.role == 'advertiser':
        # Afficher la liste des influenceurs
        influencers = InfluencerProfile.objects.all().order_by('-created_at')
        
        paginator = Paginator(influencers, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'page_obj': page_obj,
            'influencers': page_obj,
            'user_role': 'advertiser',
        }
        return render(request, 'core/home.html', context)
    
    elif request.user.role == 'influencer':
        # Afficher la liste des annonceurs
        advertisers = AdvertiserProfile.objects.all().order_by('-created_at')
        
        paginator = Paginator(advertisers, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'page_obj': page_obj,
            'advertisers': page_obj,
            'user_role': 'influencer',
        }
        return render(request, 'core/home.html', context)
    
    else:
        # Admin ou autre rôle
        return render(request, 'core/landing.html')


@cache_page(60 * 30)  # Cache 30 minutes
def about(request):
    return render(request, 'core/about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Ici vous pouvez ajouter la logique d'envoi d'email
            messages.success(request, 'Votre message a été envoyé avec succès! Nous vous répondrons bientôt.')
            form = ContactForm()
    else:
        form = ContactForm()
    
    return render(request, 'core/contact.html', {'form': form})

