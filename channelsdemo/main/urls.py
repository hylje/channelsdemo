from django.conf.urls import url

from channelsdemo.main.views import (
    thread_index, show_thread, post_post, post_thread
)

urlpatterns = [
    url(r"^$", thread_index, name="thread-index"),
    url(r"^(?P<thread_id>\d+)/$", show_thread, name="thread"),
    url(r"^(?P<thread_id>\d+)/(?P<thread_slug>[\w-]+)/$", show_thread, name="thread"),
    url(r'^post/(?P<thread_id>\d+)/$', post_post, name="post"),
    url(r'^post/$', post_thread, name="post-thread"),
]
