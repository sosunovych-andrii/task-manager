from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse

from core.models import Position, Project
from core.views.user_views import MyProfileView


class SignUpViewTests(TestCase):
    def test_view_sign_up_page(self):
        response = self.client.get(reverse("core:sign-up"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/sign_up.html")

    def test_post_sign_up_with_valid_data(self):
        response = self.client.post(
            reverse("core:sign-up"),
            data={
                "username": "user",
                "email": "example@gmail.com",
                "password1": "ytrewq123",
                "password2": "ytrewq123",
            }
        )
        self.assertTrue(get_user_model().objects.filter(username="user").exists())
        self.assertRedirects(response, "/")

    def test_post_sign_up_with_invalid_password_confirmation(self):
        response = self.client.post(
            reverse("core:sign-up"),
            data={
                "username": "user",
                "email": "example@gmail.com",
                "password1": "ytrewq123",
                "password2": "password123",
            }
        )
        self.assertNotEqual(response.status_code, 302)
        self.assertFalse(get_user_model().objects.filter(username="user").exists())


class MyProfileViewTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="TestPosition",
        )
        self.project = Project.objects.create(
            name="TestProject", description="Description for TestProject"
        )
        self.user = get_user_model().objects.create_user(
            username="user",
            password="ytrewq123",
            email="example@gmail.com",
            position=self.position,
            project=self.project,
        )

    def test_redirect_for_not_logged_in_users(self):
        response = self.client.get(reverse("core:my-profile"))
        self.assertNotEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "core/my_profile.html")

    def test_success_for_logged_in_users(self):
        self.client.login(username="user", password="ytrewq123")
        response = self.client.get(reverse("core:my-profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/my_profile.html")

    def test_get_object_returns_request_user(self):
        request = RequestFactory().get(reverse("core:my-profile"))
        request.user = self.user
        view = MyProfileView()
        view.request = request
        obj = view.get_object()
        self.assertEqual(obj, self.user)

    def test_post_method(self):
        self.client.login(username="user", password="ytrewq123")
        new_email = "new_example@gmail.com"
        new_username = "new_username"
        new_position = Position.objects.create(name="NewPosition")
        new_project = Project.objects.create(
            name="NewProject", description="Description for NewProject"
        )
        self.client.post(
            reverse("core:my-profile"),
            data={
                "username": new_username,
                "email": new_email,
                "position": new_position.id,
                "project": new_project.id,
            },
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, new_username)
        self.assertEqual(self.user.email, new_email)
        self.assertEqual(self.user.position, new_position)
        self.assertEqual(self.user.project, new_project)
