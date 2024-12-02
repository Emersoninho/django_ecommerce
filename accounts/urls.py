from django.urls import path
from . import views
from django.contrib.auth import views as auth_views #importa as views de login e logout padrão do djangp

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login',),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout_confirmation/', views.logout_confirmation, name='logout_confirmation'),
    path('register/', views.register, name='register')
]

