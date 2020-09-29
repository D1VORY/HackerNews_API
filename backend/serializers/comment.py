from rest_framework import serializers
from backend.models import Comment, Post


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["author", "created", "id"]

    def create(self, validated_data):
        """
        creates new comment
        """

        return Comment.objects.create(
            content=validated_data["content"],
            post=validated_data["post"],
            author=self._get_current_user(),
        )

    def _get_current_user(self):
        request = self.context.get("request", None)
        if request and request.user.is_authenticated:
            return request.user
        return AnonymousUser()
