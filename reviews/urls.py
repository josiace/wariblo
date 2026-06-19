from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:application_pk>/', views.create_review, name='create_review'),
    path('my-reviews/', views.user_reviews, name='user_reviews'),
]
