from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField()
    created = models.DateTimeField(auto_now_add=True, verbose_name="date of creation")
    upvotes = models.ManyToManyField(User, blank=True, related_name="upvoted_posts")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    @property
    def upvotes_count(self):
        return self.upvotes.all().count()

    def __str__(self):
        return f"{self.title}"

    def __repr__(self):
        return self.__str__()
