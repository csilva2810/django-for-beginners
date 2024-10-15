from django import template

from articles.services import is_article_owner as is_article_owner_service

register = template.Library()


@register.simple_tag(takes_context=True)
def is_article_owner(context):
    return is_article_owner_service(
        context["request"],
        context["article"],
    )
