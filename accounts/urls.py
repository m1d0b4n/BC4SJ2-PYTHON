from django.urls import path
from .views import login_view, logout_view, profile_view, register_view, edit_profile

urlpatterns = [
    path('', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('profile', profile_view, name='profile'),
    path('register', register_view, name='register'),
    path('edit_profile', edit_profile, name='edit_profile'),
]
 