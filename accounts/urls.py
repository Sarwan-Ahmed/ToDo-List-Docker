from django.urls import path, include
from . import views



urlpatterns = [
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('verify-email/<str:token>/', views.VerifyEmail.as_view(), name="verify-email"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    path('resend-link/', views.ResendLink.as_view(), name='resend-link'),
    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
