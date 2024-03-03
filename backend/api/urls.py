from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import (
    LoginView,
    LogoutView,
    UserViewSet
)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/token/login/', LoginView.as_view(), name='login'),
    path('auth/token/logout/', LogoutView.as_view(), name='logout'),
    path('auth/', include('djoser.urls.authtoken')),
]
