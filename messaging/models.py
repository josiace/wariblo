from django.db import models
from accounts.models import User


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'
        ordering = ['updated_at']
        indexes = [
            models.Index(fields=['updated_at']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        participant_names = ', '.join([user.email for user in self.participants.all()])
        return f"Conversation: {participant_names}"
    
    @property
    def last_message(self):
        return self.messages.last()
    
    def unread_count_for_user(self, user):
        return self.messages.filter(is_read=False).exclude(sender=user).count()


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
            models.Index(fields=['sender', 'created_at']),
            models.Index(fields=['is_read']),
        ]
    
    def __str__(self):
        return f"{self.sender.email}: {self.content[:50]}..."


class MessageReport(models.Model):
    """Signalement de message suspect"""
    REPORT_REASONS = [
        ('contact_info', 'Échange de coordonnées'),
        ('spam', 'Spam'),
        ('harassment', 'Harcèlement'),
        ('inappropriate', 'Contenu inapproprié'),
        ('other', 'Autre'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('reviewed', 'En cours de révision'),
        ('resolved', 'Résolu'),
        ('dismissed', 'Rejeté'),
    ]
    
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='reports')
    reason = models.CharField(max_length=50, choices=REPORT_REASONS)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports_reviewed')
    
    class Meta:
        verbose_name = 'Signalement de message'
        verbose_name_plural = 'Signalements de messages'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['reporter', 'created_at']),
        ]
    
    def __str__(self):
        return f"Signalement par {self.reporter.email} - {self.get_reason_display()}"
