from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    created = models.DateTimeField(auto_now_add=True, verbose_name="date of creation")

    def __str__(self):
        return f"{self.content}"[:40]

    def __repr__(self):
        return self.__str__()
