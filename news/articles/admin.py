from django.contrib import admin

# Register your models here.
from .models import Article, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    model = Article

    list_display = (
        "title",
        "body",
        "date",
        "author",
    )

    inlines = [
        CommentInline,
    ]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
