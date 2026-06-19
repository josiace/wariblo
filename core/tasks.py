from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def send_welcome_email(user_id):
    """
    Envoyer un email de bienvenue à un nouvel utilisateur
    """
    try:
        user = User.objects.get(id=user_id)
        subject = 'Bienvenue sur Wariblo!'
        message = render_to_string('emails/welcome.txt', {'user': user})
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return f"Email de bienvenue envoyé à {user.email}"
    except User.DoesNotExist:
        return f"Utilisateur avec ID {user_id} non trouvé"
    except Exception as e:
        return f"Erreur lors de l'envoi de l'email: {str(e)}"


@shared_task
def send_application_notification(application_id):
    """
    Envoyer une notification quand une influenceur postule à une campagne
    """
    try:
        from applications.models import Application
        application = Application.objects.select_related(
            'influencer__user', 
            'campaign__advertiser__user'
        ).get(id=application_id)
        
        advertiser_email = application.campaign.advertiser.user.email
        subject = f"Nouvelle candidature pour {application.campaign.title}"
        message = render_to_string('emails/new_application.txt', {
            'application': application,
            'campaign': application.campaign,
            'influencer': application.influencer,
        })
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [advertiser_email],
            fail_silently=False,
        )
        return f"Notification envoyée à {advertiser_email}"
    except Application.DoesNotExist:
        return f"Application avec ID {application_id} non trouvée"
    except Exception as e:
        return f"Erreur lors de l'envoi de la notification: {str(e)}"


@shared_task
def send_application_status_notification(application_id):
    """
    Envoyer une notification quand le statut d'une candidature change
    """
    try:
        from applications.models import Application
        application = Application.objects.select_related(
            'influencer__user',
            'campaign'
        ).get(id=application_id)
        
        influencer_email = application.influencer.user.email
        subject = f"Votre candidature pour {application.campaign.title}"
        
        status_messages = {
            'accepted': 'a été acceptée',
            'rejected': 'a été rejetée',
            'withdrawn': 'a été retirée',
        }
        
        message = render_to_string('emails/application_status.txt', {
            'application': application,
            'campaign': application.campaign,
            'status_message': status_messages.get(application.status, 'a changé de statut'),
        })
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [influencer_email],
            fail_silently=False,
        )
        return f"Notification de statut envoyée à {influencer_email}"
    except Application.DoesNotExist:
        return f"Application avec ID {application_id} non trouvée"
    except Exception as e:
        return f"Erreur lors de l'envoi de la notification: {str(e)}"


@shared_task
def cleanup_old_messages(days=30):
    """
    Nettoyer les anciens messages (plus de X jours)
    """
    try:
        from messaging.models import Message
        from django.utils import timezone
        from datetime import timedelta
        
        cutoff_date = timezone.now() - timedelta(days=days)
        old_messages = Message.objects.filter(created_at__lt=cutoff_date)
        count = old_messages.count()
        old_messages.delete()
        
        return f"{count} anciens messages supprimés"
    except Exception as e:
        return f"Erreur lors du nettoyage: {str(e)}"


@shared_task
def update_campaign_statistics():
    """
    Mettre à jour les statistiques des campagnes
    """
    try:
        from campaigns.models import Campaign
        from django.db.models import Count
        
        campaigns = Campaign.objects.annotate(
            applications_count=Count('applications')
        )
        
        updated_count = 0
        for campaign in campaigns:
            # Ici vous pouvez ajouter des calculs de statistiques plus complexes
            updated_count += 1
        
        return f"Statistiques mises à jour pour {updated_count} campagnes"
    except Exception as e:
        return f"Erreur lors de la mise à jour des statistiques: {str(e)}"
