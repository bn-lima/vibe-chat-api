from django.urls import include, path
from .views import Register, Login, Logout, ChangePasswordRequest, ChangePassword

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('password/', include([
        path('change/', include([
            path('', ChangePassword.as_view(), name='change'),
            path('request/', ChangePasswordRequest.as_view(), name='request')
        ]))
    ]))
]