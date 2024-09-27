from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


# Create your tests here.
class BlogTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(
            username="testuser",
            email="test@email.com",
            password="secret",
        )

        cls.post = Post.objects.create(
            title="Post title",
            body="Post content",
            author=cls.user,
        )

    def test_post_model(self):
        self.assertEqual(self.post.title, "Post title")
        self.assertEqual(self.post.body, "Post content")
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(str(self.post), "Post title")
        self.assertEqual(self.post.get_absolute_url(), f"/posts/{self.post.pk}/")

    def test_homepage(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "post_list.html")

        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.author.get_full_name())
        self.assertContains(
            response, f'<a href="{self.post.get_absolute_url()}">Read</a>'
        )

    def test_post_detail(self):
        home_url = reverse("home")
        post_detail_url = reverse("post_detail", kwargs={"pk": self.post.pk})
        response = self.client.get(post_detail_url)

        self.assertTemplateUsed(response, "post_detail.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.author.get_full_name())
        self.assertContains(response, f'<a href="{home_url}">Blog</a>')

    def test_post_detail_404(self):
        post_detail_url = reverse("post_detail", kwargs={"pk": 1000})
        response = self.client.get(post_detail_url)
        self.assertEquals(response.status_code, 404)

    def test_post_create_view(self):
        response = self.client.post(
            reverse("post_create"),
            {
                "title": "Test post",
                "body": "Test post",
                "author": self.user.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        created_post = Post.objects.last()
        self.assertEqual(created_post.title, "Test post")
        self.assertEqual(created_post.body, "Test post")
        self.assertEqual(created_post.author.id, self.user.id)

    def test_post_edit_view(self):
        post = Post.objects.create(
            title="Test post",
            body="Test post",
            author=self.user,
        )

        response = self.client.post(
            reverse("post_edit", args=(post.pk,)),
            {
                "title": "Test post (edited)",
                "body": "Test post (edited)",
            },
        )
        self.assertEqual(response.status_code, 302)

        post.refresh_from_db()
        self.assertEqual(post.title, "Test post (edited)")
        self.assertEqual(post.body, "Test post (edited)")

    def test_post_delete_view(self):
        post = Post.objects.create(
            title="Test post",
            body="Test post",
            author=self.user,
        )
        response = self.client.post(
            reverse("post_delete", args=(post.pk,)),
        )
        self.assertEqual(response.status_code, 302)

        post = Post.objects.filter(pk=post.pk).first()
        self.assertIsNone(post)
