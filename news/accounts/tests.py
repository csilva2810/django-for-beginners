from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class UserManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass1234",
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username="testsuperuser",
            email="testsuperuser@example.com",
            password="testpass1234",
        )
        self.assertEqual(user.username, "testsuperuser")
        self.assertEqual(user.email, "testsuperuser@example.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class TestSignUp(TestCase):
    def test_with_correct_template(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_user(self):
        User = get_user_model()
        user = {
            "username": "testuser",
            "email": "testuser@gmail.com",
            "age": 33,
            "password1": "testdjango123",
            "password2": "testdjango123",
        }
        response = self.client.post(
            reverse("signup"),
            user,
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        db_user = User.objects.get(username=user["username"])
        self.assertEqual(db_user.email, user["email"])
        self.assertEqual(db_user.age, user["age"])
        self.assertEqual(db_user.is_staff, False)
        self.assertEqual(db_user.is_superuser, False)
