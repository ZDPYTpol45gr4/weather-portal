from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.home, name="home"),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="register/password_reset.html"),
         name="reset_password"),
    path('reset_password_send/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/,<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
