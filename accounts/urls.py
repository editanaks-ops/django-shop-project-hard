from django.urls import path
from .views import register, activate, login_view, logout_view, profile, delete_account

urlpatterns = [
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('delete/', delete_account, name='delete_account'),
]