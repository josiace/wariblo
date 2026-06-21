from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('pricing/', views.pricing_plans, name='pricing_plans'),
    path('subscribe/<int:plan_id>/', views.subscribe, name='subscribe'),
    path('subscription/success/', views.subscription_success, name='subscription_success'),
    path('subscription/my/', views.my_subscription, name='my_subscription'),
    path('subscription/cancel/<int:subscription_id>/', views.cancel_subscription, name='cancel_subscription'),
    path('transactions/', views.transactions_history, name='transactions_history'),
]
