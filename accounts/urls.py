from django.urls import include, path
from .views import Register, Login, Logout, ChangePasswordRequest, ChangePassword, ForgotPassword

urlpatterns = [
    path('register/', Register.as_view(), name='register'), # Criar usuário
    path('login/', Login.as_view(), name='login'), # Login com token
    path('logout/', Logout.as_view(), name='logout'), # Logout, invalida token

    path('password/', include([
        path('change/', include([
            path('', ChangePassword.as_view(), name='change'), # Alterar senha com token
            path('forgot/', ForgotPassword.as_view(), name='forgot'), # Solicitar reset de senha (não logado)
            path('request/', ChangePasswordRequest.as_view(), name='request') # Solicitar reset de senha (logado)
        ]))
    ]))
]