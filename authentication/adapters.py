# authentication/adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class ForcedPasswordAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        if not user.has_usable_password():
            request.session['force_password_setup'] = True
            request.session.modified = True  # Force la sauvegarde
        return user