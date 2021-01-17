from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.logout_page, name='logout'),
    path('activate/<uidb64>/<token>/', views.confirm_email_verification_view, name='confirm_email_verification'),
    path("password_reset", views.PasswordResetRequestView.as_view(), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset/password_reset_complete.html'),
         name='password_reset_complete'),
]
