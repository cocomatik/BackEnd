# from django.contrib.auth import logout
# from django.shortcuts import redirect
# from django.conf import settings
# class SessionAuthOnlyMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         excluded_paths = ('/', '/accounts/login/','/api/')  
#         if request.path in excluded_paths:
#             return self.get_response(request)

#         if not request.user.is_authenticated:
#             return redirect(settings.LOGIN_URL)

#         if request.headers.get('Authorization'):
#             logout(request)
#             return redirect(settings.LOGIN_URL)

#         return self.get_response(request)
