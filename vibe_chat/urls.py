from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('chatroom/', include("chat.urls")),
    path('profile/', include('account_profile.urls'))
]
