from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, mixins
from rest_framework.decorators import api_view, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from api_yamdb import settings
from .filters import TitleFilter
from .models import Review, User, Title, Category, Genre
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAdminOrModer
from .serializers import ReviewSerializer, CommentSerializer, EmailSerializer, UserSerializer, CategorySerializer, \
    GenreSerializer, TitleSerializer


@api_view(['POST'])
def get_conf_code(request):
    email = request.data.get('email')
    user = get_object_or_404(User, email=email)
    if User.objects.filter(email=email).exists():
        confirmation_code = default_token_generator.make_token(user)
        mail_subject = 'Код подтверждения '
        message = f'Твой код для регистрации: {confirmation_code}'
        from_email = settings.EMAIL_HOST_USER
        to_email = email
        send_mail(
            mail_subject, message,
            from_email,
            [to_email],
        )
        return Response(f'Вам был выслан код для регистрации на {email}', status=200)


@api_view(['POST'])
def get_token(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, email=email)
    if default_token_generator.check_token(user, code):
        access = AccessToken.for_user(user)
        refresh = RefreshToken.for_user(user)
        return Response({'AccessToken': f'{access}', 'RefreshToken': f'{refresh}'}, status=200)
    return Response(status=400)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdmin, IsAuthenticated,)
    pagination_class = PageNumberPagination
    lookup_field = 'username'

    @action(detail=False, methods=['PATCH', 'GET'],
            permission_classes=(IsAuthenticated,))
    def me(self, request, ):
        serializer = UserSerializer(request.user,
                                    data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'

    def get_queryset(self):
        return Category.objects.all()


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'

    def get_queryset(self):
        return Genre.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly]

    def category_genre_perform(self, serializer):
        category_slug = self.request.data['category']
        category = get_object_or_404(Category, slug=category_slug)
        genre_slug = self.request.POST.getlist('genre')
        genres = Genre.objects.filter(slug__in=genre_slug)
        serializer.save(
            category=category,
            genre=genres,
        )

    def perform_create(self, serializer):
        self.category_genre_perform(serializer)

    def perform_update(self, serializer):
        self.category_genre_perform(serializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrModer, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def serializing_and_rating_calculation(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, title=title)
        title.rating = (Review.objects.filter(title=title).aggregate(Avg(
            'score'))['score__avg'])
        title.save(update_fields=['rating'])

    def perform_create(self, serializer):
        self.serializing_and_rating_calculation(serializer)

    def perform_update(self, serializer):
        self.serializing_and_rating_calculation(serializer)

    def get_serializer_context(self):
        return {'title_id': self.kwargs['title_id'], 'request': self.request}


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrModer, IsAuthenticatedOrReadOnly]

    def get_review(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title__id=title_id)
        return review

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)
