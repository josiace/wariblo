from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:campaign_pk>/', views.application_create, name='application_create'),
    path('<int:pk>/', views.application_detail, name='application_detail'),
    path('<int:pk>/accept/', views.application_accept, name='application_accept'),
    path('<int:pk>/reject/', views.application_reject, name='application_reject'),
    path('<int:pk>/withdraw/', views.application_withdraw, name='application_withdraw'),
    path('campaign/<int:campaign_pk>/', views.campaign_applications, name='campaign_applications'),
]
