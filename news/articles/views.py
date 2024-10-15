from typing import Union
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView,
)

from articles.services import is_article_owner

from .models import Article


class IsArticleOwnerMixin(UserPassesTestMixin):
    """
    Protects a delete/update view from being accessed by a user who is not its
    owner (author), assuring that only the owner of an article is able to
    delete/update it
    """

    def test_func(self: Union[UpdateView, DeleteView]):
        return is_article_owner(self.request, self.get_object())


# Create your views here.,
class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "articles/article_list.html"
    context_object_name = "articles"


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = "articles/article_detail.html"
    context_object_name = "article"


class ArticleUpdateView(LoginRequiredMixin, IsArticleOwnerMixin, UpdateView):
    model = Article
    template_name = "articles/article_edit.html"
    fields = (
        "title",
        "body",
    )


class ArticleDeleteView(LoginRequiredMixin, IsArticleOwnerMixin, DeleteView):
    model = Article
    template_name = "articles/article_delete.html"
    success_url = reverse_lazy("article_list")


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "articles/article_create.html"
    success_url = reverse_lazy("article_list")
    fields = (
        "title",
        "body",
    )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
