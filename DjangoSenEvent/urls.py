
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    
    path('', include('homepage.urls')),
    path("authent/", include("authentication.urls")),
    path('accounts/', include('allauth.urls')),

    path("profiles/", include("profiles.urls")),


    path('Events/', include('events.urls')),
    path('CreateEvent/', include('CreateEvent.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    



