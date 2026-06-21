from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.core.paginator import Paginator

from accounts.models import User
from core.models import Subscription, SubscriptionPlan, Transaction, PaymentMethod, ManualPayment


@login_required
def pricing_plans(request):
    """Afficher les plans d'abonnement disponibles"""
    user_type = "influencer" if request.user.is_influencer else "advertiser"
    plans = SubscriptionPlan.objects.filter(
        user_type=user_type, is_active=True
    ).order_by("price")

    # Obtenir l'abonnement actuel de l'utilisateur
    current_subscription = request.user.subscriptions.filter(
        status="active", end_date__gt=timezone.now()
    ).first()

    context = {
        "plans": plans,
        "current_subscription": current_subscription,
        "user_type": user_type,
    }
    return render(request, "billing/pricing_plans.html", context)


@login_required
def subscribe(request, plan_id):
    """S'abonner à un plan avec paiement manuel"""
    plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)

    # Vérifier que le plan correspond au type d'utilisateur
    user_type = "influencer" if request.user.is_influencer else "advertiser"
    if plan.user_type != user_type:
        messages.error(
            request, "Ce plan n'est pas disponible pour votre type de compte."
        )
        return redirect("billing:pricing_plans")

    # Vérifier si l'utilisateur a déjà un paiement en attente pour ce plan
    existing_payment = ManualPayment.objects.filter(
        user=request.user,
        subscription_plan=plan,
        status='pending'
    ).first()
    
    if existing_payment:
        messages.warning(request, "Vous avez déjà une demande de paiement en attente pour ce plan.")
        return redirect('billing:my_subscription')

    # Récupérer les méthodes de paiement actives
    payment_methods = PaymentMethod.objects.filter(is_active=True)

    if request.method == "POST":
        payment_method_id = request.POST.get('payment_method')
        transaction_reference = request.POST.get('transaction_reference')
        payment_date = request.POST.get('payment_date')
        notes = request.POST.get('notes')
        proof_document = request.FILES.get('proof_document')
        
        if not payment_method_id:
            messages.error(request, "Veuillez sélectionner une méthode de paiement.")
            return render(request, 'billing/request_subscription.html', {
                'plan': plan,
                'payment_methods': payment_methods,
            })
        
        payment_method = get_object_or_404(PaymentMethod, pk=payment_method_id)
        
        # Créer le paiement manuel
        payment = ManualPayment.objects.create(
            user=request.user,
            subscription_plan=plan,
            payment_method=payment_method,
            amount=plan.price,
            currency=plan.currency,
            transaction_reference=transaction_reference,
            payment_date=payment_date if payment_date else None,
            notes=notes,
            proof_document=proof_document,
            status='pending'
        )
        
        messages.success(request, "Votre demande de paiement a été soumise. Nous traiterons votre demande sous peu.")
        return redirect('billing:my_subscription')

    context = {
        'plan': plan,
        'payment_methods': payment_methods,
    }
    return render(request, 'billing/request_subscription.html', context)


@login_required
def subscription_success(request):
    """Page de confirmation d'abonnement"""
    subscription = request.user.subscriptions.filter(
        status="active", end_date__gt=timezone.now()
    ).first()

    if not subscription:
        return redirect("pricing_plans")

    context = {
        "subscription": subscription,
    }
    return render(request, "billing/subscription_success.html", context)


@login_required
def my_subscription(request):
    """Afficher l'abonnement actuel de l'utilisateur et les paiements en attente"""
    subscription = request.user.subscriptions.filter(
        status="active", end_date__gt=timezone.now()
    ).first()

    # Récupérer les paiements en attente
    pending_payments = ManualPayment.objects.filter(
        user=request.user,
        status='pending'
    ).order_by('-created_at')
    
    # Récupérer tous les paiements
    all_payments = ManualPayment.objects.filter(
        user=request.user
    ).order_by('-created_at')
    
    paginator = Paginator(all_payments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Historique des transactions
    transactions = request.user.transactions.all()[:10]

    context = {
        "subscription": subscription,
        "pending_payments": pending_payments,
        "page_obj": page_obj,
        "transactions": transactions,
    }
    return render(request, "billing/my_subscription.html", context)


@login_required
def cancel_subscription(request, subscription_id):
    """Annuler l'abonnement"""
    subscription = get_object_or_404(
        Subscription, id=subscription_id, user=request.user
    )

    if subscription.status != "active":
        messages.error(request, "Cet abonnement n'est pas actif.")
        return redirect("my_subscription")

    if request.method == "POST":
        subscription.status = "cancelled"
        subscription.auto_renew = False
        subscription.save()

        messages.success(
            request,
            "Votre abonnement a été annulé. Il restera actif jusqu'à la fin de la période.",
        )
        return redirect("my_subscription")

    context = {
        "subscription": subscription,
    }
    return render(request, "billing/cancel_subscription.html", context)


@login_required
def transactions_history(request):
    """Afficher l'historique des transactions"""
    transactions = request.user.transactions.all().order_by("-created_at")

    context = {
        "transactions": transactions,
    }
    return render(request, "billing/transactions_history.html", context)
