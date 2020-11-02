from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import ReviewViewSet, CommentViewSet, get_conf_code, get_token, UserViewSet


v1_router = DefaultRouter()
v1_router.register(r'users', UserViewSet,)
v1_router.register(r'titles/(?P<title_id>[0-9]+)/reviews', ReviewViewSet, basename='reviews')
v1_router.register(r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/auth/email/', get_conf_code),
    path('v1/auth/token/', get_token, name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/', include(v1_router.urls)),
]

