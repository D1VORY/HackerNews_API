from django.urls import path
from rest_framework.routers import DefaultRouter
from backend.views import PostViewSet, CommentViewSet


urlpatterns = []
router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")
urlpatterns += router.urls
