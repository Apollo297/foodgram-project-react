from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ingredients.views import IngredientViewSet
from recipes.views import RecipeViewSet
from tags.views import TagViewSet
from users.views import (
    LoginView,
    LogoutView,
    UserViewSet
)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(
    r'ingredients',
    IngredientViewSet,
    basename='ingredients'
)
router_v1.register(
    r'recipes',
    RecipeViewSet,
    basename='recipes'
)
router_v1.register(
    r'users',
    UserViewSet,
    basename='users'
)
router_v1.register(
    r'tags',
    TagViewSet,
    basename='tag'
)

urlpatterns = [
    path('', include(router_v1.urls)),
    path(
        'auth/token/login/',
        LoginView.as_view(),
        name='login'
    ),
    path(
        'auth/token/logout/',
        LogoutView.as_view(),
        name='logout'
    ),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
