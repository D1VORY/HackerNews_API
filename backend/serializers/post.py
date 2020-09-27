from rest_framework import serializers
from backend.models import Post
from django.contrib.auth.models import User
from rest_framework.serializers import raise_errors_on_nested_writes
import copy


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username")
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

        request = self.context.get("request", None)
        if request and request.user.is_authenticated:
            return obj.upvotes.filter(pk=request.user.id).exists()

        return False

    def create(self, validated_data):
        return Post.objects.create(
            title=validated_data["title"],
            link=validated_data["link"],
            author=User.objects.get(username=validated_data["author"]["username"]),
        )

    def update(self, instance, validated_data):
        """
        performs update of instance
        """

        upd_dict = copy.deepcopy(validated_data)  # to not modify validated data
        try:
            # to update nested fields
            upd_dict["author"] = User.objects.get(
                username=upd_dict["author"]["username"]
            )
        except KeyError:
            upd_dict.pop("author", None)

        for attr, value in upd_dict.items():
            setattr(instance, attr, value)
        instance.save()

        # p.s. I know this is a bad way to do this, but didn't find a
        # proper solution for updating nested fields
        return instance
