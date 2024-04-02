from django.contrib import admin
from django.urls import path

from account.views import RegisterView, LoginView, UserProfileDetailView, UserListView, UserDetailView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', UserProfileDetailView.as_view(), name='profile-detail'),
    path('users/', UserListView.as_view(), name='users-list'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
]
