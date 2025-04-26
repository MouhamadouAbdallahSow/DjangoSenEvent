from django.urls import path, include
from . import views

app_name = "authentication"

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("choose-profile/", views.choose_profile_view, name="choose_profile"),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('set-password/', views.set_password_view, name='set_password'),
    path("", include("django.contrib.auth.urls")),
]
