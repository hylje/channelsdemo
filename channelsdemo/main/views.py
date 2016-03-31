from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.utils.timezone import now
from django.template import loader

from channels import Group

from channelsdemo.main.forms import PostForm, ThreadForm
from channelsdemo.main.models import Thread, Post


def thread_index(request):
    return render(
        request,
        "main/index.html",
        {
            "threads": Thread.objects.all(),
            "thread_form": ThreadForm(prefix="thread"),
            "post_form": PostForm(prefix="post"),
        }
    )

def show_thread(request, thread_id, thread_slug):
    thread = get_object_or_404(Thread, pk=thread_id)

    if thread_slug != slugify(thread.title):
        return redirect(thread.get_absolute_url())

    return render(
        request,
        "main/thread.html",
        {
            "thread": thread,
            "post_form": PostForm()
        }
    )

def post_thread(request):
    if request.method != "POST":
        return redirect("thread-index")

    thread_form = ThreadForm(request.POST, prefix="thread")
    post_form = PostForm(request.POST, request.FILES, prefix="post")
    if thread_form.is_valid() and post_form.is_valid():
        thread = thread_form.save()
        post = post_form.save(commit=False)
        post.thread = thread
        post.save()
        messages.success(request, "Posted successfully!")
        Group("board").send({
            "text": "New thread has been posted!"
        })
        return redirect(thread.get_absolute_url())
    messages.error(request, "Error posting thread.")
    return redirect("thread-index")

def post_post(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)

    if request.method != "POST":
        return redirect(thread.get_absolute_url())

    post_form = PostForm(request.POST, request.FILES)
    if post_form.is_valid():
        post = post_form.save(commit=False)
        post.thread = thread
        post.save()
        thread.bumped = now()
        thread.save()
        messages.success(request, "Posted successfully!")
        Group("thread-%s" % thread.pk).send({
            "text": unicode(loader.get_template("main/snippets/post.html").render({
                "post": post
            }))
        })
        Group("board").send({
            "text": "A thread has been bumped!"
        })
        return redirect(post.get_absolute_url())

    messages.error(request, "Error posting to thread.")
    return redirect(thread.get_absolute_url())
