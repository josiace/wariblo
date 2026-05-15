from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def influencer_required(view_func):
    """Decorator to restrict view to influencers only"""
    @login_required
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_influencer:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapped_view


def advertiser_required(view_func):
    """Decorator to restrict view to advertisers only"""
    @login_required
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_advertiser:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapped_view


def admin_required(view_func):
    """Decorator to restrict view to admins only"""
    @login_required
    def wrapped_view(request, *args, **kwargs):
        if not (request.user.is_admin_user or request.user.is_superuser):
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapped_view
