from django.urls import path
from rest_framework.routers import DefaultRouter
from backend.views import PostViewSet, CommentViewSet, upvote_post, PostRelatedComments


urlpatterns = [
    path("posts/<int:post_id>/upvote/", upvote_post, name="upvote post"),
    path(
        "posts/<int:post_id>/comments/",
        PostRelatedComments.as_view(),
        name="relatedcomments",
    ),
]
router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")
urlpatterns += router.urls
