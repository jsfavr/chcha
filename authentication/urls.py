from django.urls import path
from .views import RegisterView,SetNewPasswordAPIview, RegisterVendorView, RegisterAdminView, RegisterPosView, RegisterDelboyView, LoginuserView, VerifyEmail, LoginvendorView, LoginadminView, LoginposView, LoginboyView, PasswordTokenCheckAPI,RequestPasswordResetEmail, PosDetailsAPIview,LoginotpuserView,LogiotpView,AuthenticationCheckView,EmailSendAPI,ForgotSendAPI,LoginotpadminView,LogiotpadminView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from . import views
# from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('userregister/', RegisterView.as_view(), name='register'),
    path('vendorregister/', RegisterVendorView.as_view(), name='vendorregister'),
    path('adminregister/', RegisterAdminView.as_view(), name='adminregister'),
    path('posregister/', RegisterPosView.as_view(), name='posregister'),
    path('delboyregister/', RegisterDelboyView.as_view(), name='delboyregister'),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('userlogin/', LoginuserView.as_view(), name='userlogin'),
    path('vendorlogin/', LoginvendorView.as_view(), name='vendorlogin'),
    path('adminlogin/', LoginadminView.as_view(), name='adminlogin'),
    path('poslogin/', LoginposView.as_view(), name='poslogin'),
    path('boylogin/', LoginboyView.as_view(), name='boylogin'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('passwod-reset-complete',SetNewPasswordAPIview.as_view(),name='passwod-reset-complete'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('posDetails/<id>',PosDetailsAPIview.as_view(),name='posDetails'),
    path('userotplogin/', LoginotpuserView.as_view(), name='userotplogin'),
    path('adminotplogin/', LoginotpadminView.as_view(), name='adminotplogin'),
    path('checkphone/', LogiotpView.as_view(), name='checkphone'),
    path('checkphoneadmin/', LogiotpadminView.as_view(), name='checkphoneadmin'),

    path('authcheck/', AuthenticationCheckView.as_view(), name='authcheck'),
    path('sendmail/',EmailSendAPI.as_view(),name="sendmail"),
    path('ForgotSendAPI/',ForgotSendAPI.as_view(),name="ForgotSendAPI"),
    path('emailView/',views.emailView,name="emailView"),
    path('updateReffer/',views.updateReffer.as_view(),name="updateReffer")


]
