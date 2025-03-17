from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import logout
from functools import wraps
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

def session_auth_required(view_func):
    """Decorator to enforce session-based authentication (no token authentication)."""
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        # Block access if Authorization header is present (token auth)
        if request.headers.get('Authorization'):
            logout(request)
            if request.path.startswith('/api/'):
                return JsonResponse({'error': 'Session authentication required'}, status=401)
            return redirect(settings.LOGIN_URL)
        
        # Require session login
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)

        return view_func(request, *args, **kwargs)
    
    return wrapped_view

def token_auth_required(view_func):
    """Decorator to enforce token-based authentication (no session authentication)."""
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        # Extract token authentication
        auth = TokenAuthentication()
        try:
            user_auth_tuple = auth.authenticate(request)
            if user_auth_tuple is None:
                raise AuthenticationFailed("Token authentication required")
            request.user = user_auth_tuple[0]  
        except AuthenticationFailed:
            return JsonResponse({'error': 'Token authentication required'}, status=401)

        return view_func(request, *args, **kwargs)

    return wrapped_view
