from .models import UserActivityLog
from django.utils.timezone import now

class ActivityLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Log activity only if the path is not excluded (e.g., static files)
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return response

        # Extract user info
        user = request.user if request.user.is_authenticated else None

        # Get IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

        # Log user activity
        UserActivityLog.objects.create(
            user=user,
            request_path=request.path,
            request_method=request.method,
            ip_address=ip,
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            additional_info={
                'GET': request.GET.dict(),
                'POST': request.POST.dict(),
            }
        )

        return response
