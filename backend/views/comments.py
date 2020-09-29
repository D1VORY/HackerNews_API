from rest_framework import viewsets, generics

from backend.serializers import CommentSerializer
from backend.models import Comment, Post
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError


class CommentViewSet(viewsets.ModelViewSet):
    """
    perform CRUD operations under posts
    """

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class PostRelatedComments(generics.ListAPIView):
    """
    returns all comments that were written to specific post
    """

    serializer_class = CommentSerializer

    def get_queryset(self):
        try:
            post = Post.objects.get(pk=self.kwargs.get("post_id", None))
        except Post.DoesNotExist:
            raise ValidationError("post does not exists")
        return post.comments.all()
