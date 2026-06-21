from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.influencer_dashboard, name='influencer_dashboard'),
    path('profile/create/', views.influencer_profile_create, name='influencer_profile_create'),
    path('profile/edit/', views.influencer_profile_edit, name='influencer_profile_edit'),
    path('campaigns/', views.influencer_campaigns, name='influencer_campaigns'),
    path('applications/', views.influencer_applications, name='influencer_applications'),
    path('list/', views.influencer_list, name='influencer_list'),
    path('<int:pk>/', views.influencer_detail, name='influencer_detail'),
]
