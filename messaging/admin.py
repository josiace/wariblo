from django.contrib import admin
from django.utils.html import format_html
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['get_id', 'get_participants', 'get_last_message', 'updated_at', 'created_at']
    filter_horizontal = ['participants']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    ordering = ['-updated_at']
    
    fieldsets = (
        ('Participants', {
            'fields': ('participants',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_id(self, obj):
        return format_html('<span style="color: #FF4500; font-weight: bold;">#{}</span>', obj.id)
    get_id.short_description = 'ID'
    
    def get_participants(self, obj):
        participants = obj.participants.all()
        if participants:
            names = [p.email for p in participants[:3]]
            if len(participants) > 3:
                names.append(f'+{len(participants) - 3}')
            return format_html('<span style="color: #666;">{}</span>', ', '.join(names))
        return '—'
    get_participants.short_description = 'Participants'
    
    def get_last_message(self, obj):
        if obj.last_message:
            preview = obj.last_message.content[:30] + '...' if len(obj.last_message.content) > 30 else obj.last_message.content
            return format_html('<span style="color: #666;">{}</span>', preview)
        return '—'
    get_last_message.short_description = 'Dernier message'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['get_conversation', 'get_sender', 'get_content', 'get_read_status', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['content', 'sender__email']
    readonly_fields = ['created_at']
    list_per_page = 30
    ordering = ['-created_at']
    
    fieldsets = (
        ('Message', {
            'fields': ('conversation', 'sender', 'content', 'is_read')
        }),
        ('Date', {
            'fields': ('created_at',)
        }),
    )
    
    def get_conversation(self, obj):
        return format_html('<span style="color: #FF4500; font-weight: bold;">#{}</span>', obj.conversation.id)
    get_conversation.short_description = 'Conversation'
    
    def get_sender(self, obj):
        return format_html('<strong>{}</strong>', obj.sender.email)
    get_sender.short_description = 'Expéditeur'
    
    def get_content(self, obj):
        preview = obj.content[:40] + '...' if len(obj.content) > 40 else obj.content
        return format_html('<span style="color: #666;">{}</span>', preview)
    get_content.short_description = 'Contenu'
    
    def get_read_status(self, obj):
        if obj.is_read:
            return format_html('<span style="color: #28a745; font-weight: bold;">✓ Lu</span>')
        return format_html('<span style="color: #FFD700; font-weight: bold;">○ Non lu</span>')
    get_read_status.short_description = 'Statut'

