from django.urls import include, path
from .views import Register

urlpatterns = [
    path('register/', Register.as_view(), name='register')
]