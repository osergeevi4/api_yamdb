from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TitleViewSet, CategoryViewSet, GenreViewSet
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


v1_router = DefaultRouter()

v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='titles_get')

# router.register('category/title/(?P<title_id>\d+)/', CategoryViewSet, basename='title_item')
# router.register(r'title/(?P<title_id>\d+)/', TitleViewSet, basename='title')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
