from django.urls import path
from .views import ProfileDetail, EditProfile

urlpatterns = [
    path("<int:pk>/detail/", ProfileDetail.as_view(), name="detail"),
    path("edit/", EditProfile.as_view(), name='edit')
]