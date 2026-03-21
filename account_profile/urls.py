from django.urls import path
from .views import ProfileDetail

urlpatterns = [
    path("<int:pk>/detail/", ProfileDetail.as_view(), name="detail")
]