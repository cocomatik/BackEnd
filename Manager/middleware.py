from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings

class SessionAuthOnlyMiddleware:
    """
    Middleware to enforce session authentication for Manager (MU) app,
    allowing only the landing page (`/`) to be accessible without authentication.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_paths = ('/', '/accounts/login/')  # Ensure login page is excluded

        # If user is already at the login page, don't redirect
        if request.path in excluded_paths:
            return self.get_response(request)

        # Redirect only if user is NOT authenticated
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)

        # Block API Token authentication in Manager routes
        if request.headers.get('Authorization'):
            logout(request)
            return redirect(settings.LOGIN_URL)

        return self.get_response(request)
