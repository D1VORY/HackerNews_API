from rest_framework import generics, viewsets

from backend.serializers import PostSerializer
from backend.models import Post


class PostViewSet(viewsets.ModelViewSet):
    """
    perform CRUD operations under posts
    """

    serializer_class = PostSerializer
    queryset = Post.objects.all()
