from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/nodes/', include('nodes.api.urls'), name='nodes'),
    path('api/profiles/', include('users.api.urls'), name='profiles'),
    path('api/drf_registration/', include('drf_registration.api.urls'), name='drf-registration'),
    path('messages_drf/', include('django_messages_drf.api.urls'), name='messages-drf'),
]