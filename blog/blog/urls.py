from django.urls import path

from .views import (
    Homepage,
    PostView,
    PostCreateView,
    PostEditView,
    PostDeleteView,
)

urlpatterns = [
    path("posts/create/", PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/edit/", PostEditView.as_view(), name="post_edit"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("posts/<int:pk>/", PostView.as_view(), name="post_detail"),
    path("", Homepage.as_view(), name="home"),
]
