from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView

from .models import Post


# def reverse_lazy(viewname, *args, **kwargs):
#     def fn():
#         return reverse(viewname=viewname, args=args, kwargs=kwargs)

#     return fn


class Homepage(ListView):
    model = Post
    template_name = "post_list.html"


class PostView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"


class PostCreateView(CreateView):
    model = Post
    template_name = "post_create.html"
    fields = ["title", "author", "body"]


class PostEditView(UpdateView):
    model = Post
    template_name = "post_edit.html"
    fields = ["title", "body"]


class PostDeleteView(DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("home")
