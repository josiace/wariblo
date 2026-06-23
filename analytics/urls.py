from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('campaigns/', views.campaign_analytics_dashboard, name='campaign_dashboard'),
    path('campaigns/<int:campaign_id>/', views.campaign_analytics_detail, name='campaign_detail'),
    path('activity/', views.user_activity_dashboard, name='user_activity'),
]
