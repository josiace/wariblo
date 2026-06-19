from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import ReviewForm
from .models import Review
from campaigns.models import Campaign
from applications.models import Application


@login_required
def create_review(request, application_pk):
    """Créer un avis après une collaboration terminée"""
    application = get_object_or_404(
        Application.objects.select_related('campaign__advertiser__user', 'influencer__user'),
        pk=application_pk
    )
    
    # Vérifier que l'utilisateur peut laisser un avis
    if application.status != 'accepted':
        messages.error(request, 'Vous ne pouvez laisser un avis que pour les collaborations acceptées.')
        return redirect('dashboard')
    
    # Déterminer qui est le reviewer
    if request.user == application.campaign.advertiser.user:
        reviewed_user = application.influencer.user
    elif request.user == application.influencer.user:
        reviewed_user = application.campaign.advertiser.user
    else:
        messages.error(request, 'Vous n\'êtes pas autorisé à laisser un avis pour cette collaboration.')
        return redirect('dashboard')
    
    # Vérifier si un avis existe déjà
    if Review.objects.filter(
        reviewer=request.user,
        reviewed_user=reviewed_user,
        campaign=application.campaign
    ).exists():
        messages.warning(request, 'Vous avez déjà laissé un avis pour cette collaboration.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.reviewed_user = reviewed_user
            review.campaign = application.campaign
            review.save()
            messages.success(request, 'Votre avis a été enregistré avec succès!')
            return redirect('dashboard')
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'application': application,
        'reviewed_user': reviewed_user,
    }
    return render(request, 'reviews/create.html', context)


@login_required
def user_reviews(request):
    """Voir les avis reçus par l'utilisateur"""
    reviews = Review.objects.filter(
        reviewed_user=request.user
    ).select_related('reviewer', 'campaign').order_by('-created_at')
    
    paginator = Paginator(reviews, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculer la moyenne
    all_reviews = Review.objects.filter(reviewed_user=request.user)
    average_rating = 0
    if all_reviews.exists():
        average_rating = sum(review.rating for review in all_reviews) / all_reviews.count()
    
    context = {
        'page_obj': page_obj,
        'reviews': page_obj,
        'average_rating': round(average_rating, 1),
        'total_reviews': all_reviews.count(),
    }
    return render(request, 'reviews/list.html', context)
