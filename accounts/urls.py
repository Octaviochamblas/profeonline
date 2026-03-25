from django.urls import path
from django.contrib.auth import views as auth_views

from .views import register_view, profile_view

urlpatterns = [
    path("registro/", register_view, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="core:home"), name="logout"),  
    path("perfil/", profile_view, name="profile"),  
    ]