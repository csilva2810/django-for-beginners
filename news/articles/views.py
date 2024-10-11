from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView,
)

from .models import Article


# Create your views here.,
class ArticleListView(ListView):
    model = Article
    template_name = "articles/article_list.html"
    context_object_name = "articles"


class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/article_detail.html"
    context_object_name = "article"


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = "articles/article_edit.html"
    fields = (
        "title",
        "body",
    )


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = "articles/article_delete.html"
    success_url = reverse_lazy("article_list")


class ArticleCreateView(CreateView):
    model = Article
    template_name = "articles/article_create.html"
    success_url = reverse_lazy("article_list")
    fields = (
        "title",
        "body",
        "author",
    )
