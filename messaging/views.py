from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from .forms import MessageForm
from .models import Conversation, Message

User = get_user_model()


@login_required
def inbox(request):
    conversations = request.user.conversations.all()
    
    context = {
        'conversations': conversations,
    }
    return render(request, 'messaging/inbox.html', context)


@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    
    if request.user not in conversation.participants.all():
        return redirect('inbox')
    
    messages = conversation.messages.all()
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            conversation.updated_at = message.created_at
            conversation.save()
            return redirect('conversation_detail', pk=conversation.pk)
    else:
        form = MessageForm()
    
    context = {
        'conversation': conversation,
        'messages': messages,
        'form': form,
    }
    return render(request, 'messaging/conversation_detail.html', context)


@login_required
def conversation_create(request, user_id):
    recipient = get_object_or_404(User, pk=user_id)
    
    if recipient == request.user:
        return redirect('inbox')
    
    existing_conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(participants=recipient).first()
    
    if existing_conversation:
        return redirect('conversation_detail', pk=existing_conversation.pk)
    
    conversation = Conversation.objects.create()
    conversation.participants.add(request.user, recipient)
    
    return redirect('conversation_detail', pk=conversation.pk)

