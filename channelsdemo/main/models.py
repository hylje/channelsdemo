from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import now
from django.template.defaultfilters import slugify
from django.core import urlresolvers


class Thread(models.Model):
    bumped = models.DateTimeField(default=now)
    title = models.CharField(max_length=100)

    def get_absolute_url(self):
        return urlresolvers.reverse(
            "thread",
            kwargs={
                "thread_id": self.pk,
                "thread_slug": slugify(self.title)
            }
        )

    def last_posts(self):
        "show some posts always excluding the first one"
        first_post = self.first_post()
        posts = list(self.post_set.order_by("-created")[:4])
        if first_post in posts:
            posts.remove(first_post)
        else:
            posts.pop()
        posts.reverse()
        return posts

    def all_last_posts(self):
        "show all posts except for the first one"
        first_post = self.first_post()
        posts = list(self.post_set.all())
        posts.pop(0)
        return posts

    def first_post(self):
        "get the first post"
        return self.post_set.earliest()

    def num_posts(self):
        ret = getattr(self, '_num_posts', None)
        if ret is None:
            self._num_posts = self.post_set.count()
        return self._num_posts

    def num_images(self):
        ret = getattr(self, '_num_images', None)
        if ret is None:
            self._num_images = self.post_set.exclude(image="").count()
        return self._num_images

    class Meta:
        ordering = ("-bumped",)

def post_image_name(instance, filename):
    return "res/%d/%s" % (instance.thread.pk, filename)

class Post(models.Model):
    thread = models.ForeignKey(Thread)
    created = models.DateTimeField(default=now)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to=post_image_name, blank=True)

    def get_absolute_url(self):
        return urlresolvers.reverse(
            "thread",
            kwargs={
                "thread_id": self.thread.pk,
                "thread_slug": slugify(self.thread.title)
            }
        ) + "#c" + unicode(self.pk)

    class Meta:
        ordering = ("created",)
        get_latest_by = "created"
