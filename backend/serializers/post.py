from rest_framework import serializers
from backend.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username")
    is_upvoted_by_current_user = serializers.SerializerMethodField(
        "_is_upvoted_by_current_user"
    )

    def _is_upvoted_by_current_user(self, obj):
        """
        checks if the post was upvoted by
        current logged in user
        """

        request = self.context.get("request", None)
        if request and request.user.is_authenticated:
            return obj.upvotes.filter(pk=request.user.id).exists()

        return False

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
        read_only = ["upvotes_count"]
