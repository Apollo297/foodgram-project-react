from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import RecipeViewSet
from users.views import (
    LoginView,
    LogoutView,
    UserViewSet
)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(r'recipes', RecipeViewSet, basename='recipes')
router_v1.register(r'users', UserViewSet, basename='users')

# extra_users_patterns = [
#     path(
#         'users/subscriptions/',
#         UserSubscriptionsView.as_view(),
#         name='user-subscriptions'
#     ),
#     path(
#         'users/<int:id>/subscribe/',
#         UserSubscribeView.as_view(),
#         name='user-subscribe'
#     ),
# ]

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/token/login/', LoginView.as_view(), name='login'),
    path('auth/token/logout/', LogoutView.as_view(), name='logout'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
