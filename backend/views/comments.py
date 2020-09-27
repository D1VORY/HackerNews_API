from rest_framework import viewsets

from backend.serializers import CommentSerializer
from backend.models import Comment


class CommentViewSet(viewsets.ModelViewSet):
    """
    perform CRUD operations under posts
    """

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
