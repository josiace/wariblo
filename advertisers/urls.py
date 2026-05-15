from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.advertiser_dashboard, name='advertiser_dashboard'),
    path('profile/create/', views.advertiser_profile_create, name='advertiser_profile_create'),
    path('profile/edit/', views.advertiser_profile_edit, name='advertiser_profile_edit'),
    path('campaigns/', views.advertiser_campaigns, name='advertiser_campaigns'),
]
