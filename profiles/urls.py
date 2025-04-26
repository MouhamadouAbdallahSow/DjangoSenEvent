
from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),
    # path('creator/', views.creator_homepage, name='creator_homepage'),
    # path('participant/', views.participant_homepage, name='participant_homepage'),
    # path('visitor/', views.visitor_homepage, name='visitor_homepage'),
]
