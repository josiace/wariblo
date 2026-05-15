from django.shortcuts import render
from django.contrib import messages
from .forms import ContactForm


def landing_page(request):
    return render(request, 'core/landing.html')


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

