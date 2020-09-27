from rest_framework import generics, viewsets

from backend.serializers import PostSerializer
from backend.models import Post
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """
    perform CRUD operations under posts
    """

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


@permission_classes([IsAuthenticated])
@api_view(["POST"])
def upvote_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({"content": "post not found"}, status=status.HTTP_404_NOT_FOUND)

    # check if post has been already upvoted by current user
    if post.upvotes.filter(pk=request.user.id).exists():
        return Response(
            {"content": "post already upvoted"}, status=status.HTTP_400_BAD_REQUEST
        )
    request.user.upvoted_posts.add(post)
    return Response({"content": "post upvoted"}, status=status.HTTP_200_OK)
