from typing import Any, Union
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView,
    FormView,
)

from articles.forms import CommentForm
from articles.services import is_article_owner

from .models import Article, Comment


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


class ArticleGetView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = "articles/article_detail.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        return context


class ArticlePostView(SingleObjectMixin, FormView):
    model = Article
    form_class = CommentForm
    template_name = "article_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(self, request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "article_detail",
            kwargs={"pk": self.object.pk},
        )


class ArticleDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = ArticleGetView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ArticlePostView.as_view()
        return view(request, *args, **kwargs)


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
