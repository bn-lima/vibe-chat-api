from django.urls import path, include
from .views import CreateChatRoom

urlpatterns = [
    path("new/", CreateChatRoom.as_view(), name="new")
]