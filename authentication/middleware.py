# authentication/middleware.py
from django.urls import reverse
from django.shortcuts import redirect

class SocialPasswordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.set_password_url = reverse('authentication:set_password')

    def __call__(self, request):
        if (
            request.user.is_authenticated
            and request.session.get('force_password_setup')
            and request.path != self.set_password_url
        ):
            return redirect(self.set_password_url)
        return self.get_response(request)