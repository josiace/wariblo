from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<int:pk>/', views.conversation_detail, name='conversation_detail'),
    path('create/<int:user_id>/', views.conversation_create, name='conversation_create'),
]
