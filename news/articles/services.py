from articles.models import Article


def is_article_owner(request, article: Article):
    return request.user.pk == article.author.pk
