from django.contrib.auth import get_user_model
from django.db.models import Count
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from core.models import Project, Position, Task, Worker
from core.views.worker_views import WorkerListView


class WorkerListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.project = Project.objects.create(
            name="ProjectName",
            description="Description for project",
        )
        cls.position = Position.objects.create(name="PositionName")
        cls.users = []
        for i in range(10):
            user = get_user_model().objects.create_user(
                username=f"user{i}",
                password=f"ytrewq123",
                project=cls.project,
                position=cls.position,
            )
            cls.users.append(user)

        cls.tasks = []
        for i in range(10):
            task = Task.objects.create(
                name=f"TaskName{i}",
                description="Description for Task",
                deadline=timezone.now() + timedelta(minutes=45),
                priority="LOW",
                project=cls.project,
                assignee=cls.users[i],
            )
            cls.tasks.append(task)

    def test_redirect_for_not_logged_in_users(self):
        response = self.client.get(reverse("core:worker-list"))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, "core/worker_list.html")

    def test_success_for_logged_in_users(self):
        self.client.login(username="user0", password="ytrewq123")
        response = self.client.get(reverse("core:worker-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/worker_list.html")

    def test_list_pagination(self):
        self.client.login(username="user0", password="ytrewq123")
        response = self.client.get(reverse("core:worker-list") + "?page=1")
        self.assertEqual(len(response.context["worker_list"]), 8)
        response = self.client.get(reverse("core:worker-list") + "?page=2")
        self.assertEqual(len(response.context["worker_list"]), 2)

    def test_get_queryset_with_valid_form(self):
        request = RequestFactory().get(
            reverse("core:worker-list") + "?position=1&project=1&username=user0"
        )
        view = WorkerListView()
        view.request = request
        queryset = view.get_queryset().values(
            "username", "tasks_count", "position", "project"
        )
        expected_queryset = (
            Worker.objects.select_related("position", "project")
            .annotate(tasks_count=Count("assigned_tasks"))
            .filter(
                position=self.position,
                project=self.project,
                username__icontains="user0",
            )
            .values("username", "tasks_count", "position", "project")
        )
        self.assertEqual(list(queryset.values()), list(expected_queryset.values()))

    def test_get_queryset_with_invalid_form(self):
        request = RequestFactory().get(
            reverse("core:worker-list") + "?position=invalid"
        )
        view = WorkerListView()
        view.request = request
        queryset = view.get_queryset().values(
            "username", "tasks_count", "position", "project"
        )
        expected_queryset = (
            Worker.objects.select_related("position", "project")
            .annotate(tasks_count=Count("assigned_tasks"))
            .values("username", "tasks_count", "position", "project")
        )
        self.assertEqual(list(queryset.values()), list(expected_queryset.values()))

    def test_get_context_data(self):
        request = RequestFactory().get(
            reverse("core:worker-list"),
            data={
                "username": self.users[0].username,
                "position": self.position,
                "project": self.project,
            },
        )
        request.user = self.users[0]
        response = WorkerListView.as_view()(request)
        self.assertIn("search_form", response.context_data)
        self.assertEqual(
            response.context_data["search_form"].initial["username"], "user0"
        )
        self.assertEqual(
            response.context_data["search_form"].initial["position"],
            str(self.position),
        )
        self.assertEqual(
            response.context_data["search_form"].initial["project"],
            str(self.project),
        )


class WorkerCreateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.regular_user = get_user_model().objects.create_user(
            username="regular_user",
            password="ytrewq123",
        )
        cls.admin = get_user_model().objects.create_superuser(
            username="admin_user",
            password="ytrewq123",
        )

    def test_redirect_for_not_logged_in_users(self):
        response = self.client.get(reverse("core:worker-create"))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, "core/worker_form.html")

    def test_permission_denied_for_logged_in_regular_users(self):
        self.client.login(username="regular_user", password="ytrewq123")
        response = self.client.get(reverse("core:worker-create"))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, "core/worker_form.html")

    def test_success_for_logged_in_admin_users(self):
        self.client.login(username="admin_user", password="ytrewq123")
        response = self.client.get(reverse("core:worker-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/worker_create_form.html")

    def test_post_method_for_admin_users(self):
        self.client.login(username="admin_user", password="ytrewq123")
        response = self.client.post(
            reverse("core:worker-create"),
            data={
                "username": "new_admin_username",
                "password1": "ytrewq123",
                "password2": "ytrewq123",
            },
        )
        self.assertRedirects(response, reverse("core:worker-list"))
        self.assertTrue(
            get_user_model().objects.filter(username="new_admin_username").exists()
        )


class WorkerUpdateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="ytrewq123",
        )
        self.admin = get_user_model().objects.create_superuser(
            username="admin_user",
            password="ytrewq123",
        )

    def test_redirect_for_not_logged_in_users(self):
        response = self.client.get(reverse("core:worker-update", args=(self.user.id,)))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, "core/worker_update_form.html")

    def test_permission_denied_for_logged_in_regular_users(self):
        self.client.login(username="user", password="ytrewq123")
        response = self.client.get(reverse("core:worker-update", args=(self.user.id,)))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed("core/worker_update_form.html")

    def test_success_for_logged_in_admin_users(self):
        self.client.login(username="admin_user", password="ytrewq123")
        response = self.client.get(reverse("core:worker-update", args=(self.admin.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("core/worker_update_form.html")

    def test_post_method_for_admin_users(self):
        self.client.login(username="admin_user", password="ytrewq123")
        new_username = "new_username"
        new_email = "new_example@gmail.com"
        self.client.post(
            reverse("core:worker-update", args=(self.user.id,)),
            data={"username": new_username, "email": new_email},
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, new_username)
        self.assertEqual(self.user.email, new_email)


class WorkerDeleteViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="ytrewq123",
        )
        self.admin = get_user_model().objects.create_superuser(
            username="admin_user",
            password="ytrewq123",
        )

    def test_redirect_for_not_logged_in_users(self):
        response = self.client.get(reverse("core:worker-delete", args=(self.user.id,)))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, "core/worker_delete.html")

    def test_permission_denied_for_logged_in_regular_users(self):
        self.client.login(username="user", password="ytrewq123")
        response = self.client.get(reverse("core:worker-delete", args=(self.user.id,)))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, "core/worker_delete.html")

    def test_success_for_logged_admin_users(self):
        self.client.login(username="admin_user", password="ytrewq123")
        response = self.client.get(reverse("core:worker-delete", args=(self.user.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("core/worker_delete.html")

    def test_post_method_for_admin_users(self):
        self.client.login(username="admin_user", password="ytrewq123")
        response = self.client.post(reverse("core:worker-delete", args=(self.user.id,)))
        self.assertRedirects(response, reverse("core:worker-list"))
        self.assertFalse(get_user_model().objects.filter(pk=self.user.id).exists())
