from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    UserListView,
    UserDetailView,
    LogoutView,
)

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('<pk>/', UserDetailView.as_view(), name='user-detail'),
    path('me/', UserDetailView.as_view(), name='current-user'),
    path('new/logout/', LogoutView.as_view(), name='new-logout'),
]
