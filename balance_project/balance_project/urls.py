from django.contrib import admin
from django.urls import path, include
from rest_framework.authentication import SessionAuthentication

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/balance/', include('balance.urls')),
]

admin.site.authentication_classes = [SessionAuthentication]
