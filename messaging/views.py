from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from .forms import MessageForm
from .models import Conversation, Message

User = get_user_model()

DEFAULT_MAX_MESSAGES_PER_DAY = 50
DEFAULT_MAX_CONVERSATIONS = 10


def get_active_subscription(user):
    """Retourner l'abonnement actif de l'utilisateur, ou None"""
    from core.models import Subscription
    return Subscription.objects.filter(
        user=user,
        status='active',
        end_date__gt=timezone.now()
    ).first()


def check_message_limits(user):
    """Verifie si l'utilisateur a atteint sa limite de messages"""
    active_subscription = get_active_subscription(user)

    # Plans payants : pas de limite
    if active_subscription and active_subscription.plan.plan_type != 'free':
        return True, None

    max_messages = (
        active_subscription.plan.max_messages if active_subscription
        else DEFAULT_MAX_MESSAGES_PER_DAY
    )

    today = timezone.now().date()
    messages_sent_today = Message.objects.filter(
        sender=user,
        created_at__date=today
    ).count()

    if messages_sent_today >= max_messages:
        return False, (
            f"Vous avez atteint votre limite de {max_messages} messages par jour. "
            "Passez à un plan payant pour envoyer plus de messages."
        )

    return True, None


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(
        participants=request.user
    ).prefetch_related(
        'participants',
        'messages__sender'
    ).distinct().order_by('-updated_at')

    # Annoter chaque conversation avec unread_count
    for conversation in conversations:
        conversation.unread_count = conversation.unread_count_for_user(request.user)

    # Recuperer la conversation active si specifiee dans l'URL
    active_conversation_id = request.GET.get('conversation')
    active_conversation = None
    if active_conversation_id:
        try:
            active_conversation = conversations.get(pk=active_conversation_id)
        except Conversation.DoesNotExist:
            pass

    context = {
        'conversations': conversations,
        'active_conversation': active_conversation,
    }
    return render(request, 'messaging/inbox.html', context)


@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(
        Conversation.objects.prefetch_related('participants', 'messages__sender'),
        pk=pk
    )

    if request.user not in conversation.participants.all():
        return redirect('inbox')

    if request.method == 'POST':
        # Verifier les limites de messages
        can_send, error_message = check_message_limits(request.user)
        if not can_send:
            messages.error(request, error_message)
            return redirect(reverse('inbox') + f'?conversation={conversation.pk}')

        form = MessageForm(request.POST, user=request.user)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            conversation.updated_at = message.created_at
            conversation.save()
            return redirect(reverse('inbox') + f'?conversation={conversation.pk}')
    else:
        # Rediriger vers inbox avec la conversation active
        return redirect(reverse('inbox') + f'?conversation={conversation.pk}')


def check_conversation_limits(user):
    """Verifie si l'utilisateur a atteint sa limite de conversations"""
    active_subscription = get_active_subscription(user)

    # Plans payants : pas de limite
    if active_subscription and active_subscription.plan.plan_type != 'free':
        return True, None

    active_conversations = Conversation.objects.filter(
        participants=user
    ).distinct().count()

    if active_conversations >= DEFAULT_MAX_CONVERSATIONS:
        return False, (
            f"Vous avez atteint votre limite de {DEFAULT_MAX_CONVERSATIONS} conversations "
            "simultanées. Passez à un plan payant pour avoir plus de conversations."
        )

    return True, None


@login_required
def conversation_create(request, user_id):
    recipient = get_object_or_404(User, pk=user_id)

    if recipient == request.user:
        return redirect('inbox')

    # Verifier les limites de conversations
    can_create, error_message = check_conversation_limits(request.user)
    if not can_create:
        messages.error(request, error_message)
        return redirect('inbox')

    existing_conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(participants=recipient).first()

    if existing_conversation:
        return redirect('conversation_detail', pk=existing_conversation.pk)

    conversation = Conversation.objects.create()
    conversation.participants.add(request.user, recipient)

    return redirect('conversation_detail', pk=conversation.pk)
