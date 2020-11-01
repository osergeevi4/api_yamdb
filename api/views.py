from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions

from .models import Review
from .serializers import ReviewSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


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
