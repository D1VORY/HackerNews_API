from rest_framework import serializers
from backend.models import Post
from django.contrib.auth.models import User
from rest_framework.serializers import raise_errors_on_nested_writes
from django.contrib.auth.models import AnonymousUser
import copy


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)
    is_upvoted_by_current_user = serializers.SerializerMethodField(
        "_is_upvoted_by_current_user"
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "link",
            "created",
            "author",
            "upvotes_count",
            "is_upvoted_by_current_user",
        ]
        read_only_fields = [
            "upvotes_count",
            "is_upvoted_by_current_user",
            "created",
            "id",
            "author",
        ]

    def validate_author(self, value):
        try:
            User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("user does not exists")

        return value

    def _is_upvoted_by_current_user(self, obj):
        """
        checks if the post was upvoted by
        current logged in user
        """
        user = self._get_current_user()
        if not user.is_anonymous:
            return obj.upvotes.filter(pk=user.id).exists()

        return False

    def create(self, validated_data):
        """
        creates new post
        """
        # due to permission_classes, user has to be authenticated
        return Post.objects.create(
            title=validated_data["title"],
            link=validated_data["link"],
            author=self._get_current_user(),
        )

    def _get_current_user(self):
        request = self.context.get("request", None)
        if request and request.user.is_authenticated:
            return request.user
        return AnonymousUser()
