from rest_framework import generics, viewsets

from backend.serializers import PostSerializer
from backend.models import Post


class PostList(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostDetail(generics.RetrieveDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
