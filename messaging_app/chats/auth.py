# messaging_app/chats/auth.py
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# You can subclass these if you want custom claims or behavior
CustomTokenObtainPairView = TokenObtainPairView
CustomTokenRefreshView = TokenRefreshView
