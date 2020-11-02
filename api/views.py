from django.shortcuts import render

from api_yamdb import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import api_view, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.viewsets import GenericViewSet


from .models import Review, User, Title, Category, Genre
from .serializers import ReviewSerializer, CommentSerializer, EmailSerializer, UserSerializer, TitleSerializer, CategorySerializer, GenreSerializer
from .permissions import IsAuthorOrReadOnly, IsAdmin, IsAdminOrReadOnly, IsAdminOrModer


class ReviewViewSet(viewsets.ModelViewSet):
    """"
    Get/Post/Put/Patch/Delete requests for reviews
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsAuthorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def get_serializer_context(self):
        context = super(ReviewViewSet, self).get_serializer_context()
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        context.update({'title': title})
        return context

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs.get("title_id"))
        serializer.save(title=title, author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    """"
    Get/Post/Put/Patch/Delete requests for comments
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsAuthorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user)


# Олег
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
      
#Дима
class TitleViewSet(viewsets.ModelViewSet):

    serializer_class = TitleSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Title.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer

    def get_queryset(self):
        return Genre.objects.all()
