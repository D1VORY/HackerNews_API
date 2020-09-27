from __future__ import absolute_import
import os
import django
from celery import Celery
from celery.schedules import crontab

# rom celery import task
from celery.decorators import periodic_task
from django.conf import settings

# from .tasks import reset_post_upvotes


# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dashboard.settings")
django.setup()


app = Celery("dashboard")

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# from .tasks import reset_post_upvotes
from backend.models import Post


@app.task
def reset_post_upvotes():
    for post in Post.objects.all():
        post.upvotes.clear()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=0, hour=0), reset_post_upvotes.s(), name="reset post upvotes"
    )
