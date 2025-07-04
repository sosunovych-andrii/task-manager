from django.contrib.auth import get_user_model
from django.db.models import Count
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from core.models import Task, Project
from core.views.project_views import ProjectListView


class ProjectListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.projects = []
        for i in range(10):
            project = Project.objects.create(
                name=f"Project{i}", description=f"Description for Project{i}"
            )
            cls.projects.append(project)

        cls.task = Task.objects.create(
            name="TaskName",
            description="Description for TaskName",
            deadline=timezone.now() + timedelta(minutes=45),
            priority="LOW",
            project=cls.projects[0],
        )
        cls.user = get_user_model().objects.create_user(
            username="user", password="ytrewq123", project=cls.projects[0]
        )

    def test_redirect_for_not_logged_in_users(self):
        response = self.client.get(reverse("core:project-list"))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, "core/project_list.html")

    def test_success_for_logged_in_users(self):
        self.client.login(username="user", password="ytrewq123")
        response = self.client.get(reverse("core:project-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/project_list.html")

    def test_list_pagination(self):
        self.client.login(username="user", password="ytrewq123")
        response = self.client.get(reverse("core:project-list"))
        self.assertEqual(len(response.context["project_list"]), 8)
        response = self.client.get(reverse("core:project-list") + "?page=2")
        self.assertEqual(len(response.context["project_list"]), 2)

    def test_get_queryset(self):
        request = RequestFactory().get(
            reverse("core:project-list"), data={"name": self.projects[0].name}
        )
        view = ProjectListView()
        view.request = request
        queryset = view.get_queryset().values("name", "workers_count", "tasks_count")
        expected_queryset = (
            Project.objects.annotate(
                workers_count=Count("workers", disctinct=True),
                tasks_count=Count("tasks", disctinct=True)
            )
            .filter(name__icontains="Project0")
            .values("name", "workers_count", "tasks_count")
        )
        self.assertEqual(list(queryset.values()), list(expected_queryset.values()))

    def test_get_context_data(self):
        request = RequestFactory().get(reverse("core:project-list") + "?name=Project0")
        request.user = self.user
        response = ProjectListView.as_view()(request)
        self.assertIn("search_form", response.context_data)
        self.assertEqual(
            response.context_data["search_form"].initial["name"], "Project0"
        )


class ProjectCreateViewTests(TestCase):
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
        response = self.client.get(reverse("core:project-create"))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, "core/project_create.html")

    def test_permission_denied_for_logged_in_users(self):
        self.client.login(username="regular_user", password="ytrewq123")
        response = self.client.get(reverse("core:project-create"))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, "core/project_form.html")

    def test_success_for_logged_in_admin_users(self):
        self.client.login(username="admin_user", password="ytrewq123")
        response = self.client.get(reverse("core:project-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("core/project_form.html")

    def test_post_method(self):
        self.client.login(username="admin_user", password="ytrewq123")
        response = self.client.post(
            reverse("core:project-create"),
            data={"name": "ProjectName", "description": "Description for ProjectName"},
        )
        self.assertRedirects(response, reverse("core:project-list"))
        self.assertTrue(Project.objects.filter(name="ProjectName").exists())


class ProjectUpdateViewTests(TestCase):
    def setUp(self):
        self.regular_user = get_user_model().objects.create_user(
            username="regular_user",
            password="ytrewq123",
        )
        self.admin = get_user_model().objects.create_superuser(
            username="admin_user",
            password="ytrewq123",
        )
        self.project = Project.objects.create(
            name="ProjectName", description="Description for ProjectName"
        )

    def test_redirect_for_not_logged_in_users(self):
        response = self.client.get(
            reverse("core:project-update", args=(self.project.id,))
        )
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, "core/project_form.html")

    def test_permission_denied_for_logged_in_regular_users(self):
        self.client.login(username="regular_user", password="ytrewq123")
        response = self.client.get(
            reverse("core:project-update", args=(self.project.id,))
        )
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed("core/project_form.html")

    def test_success_for_logged_in_admin_users(self):
        self.client.login(username="admin_user", password="ytrewq123")
        response = self.client.get(
            reverse("core:project-update", args=(self.project.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("core/project_form.html")

    def test_post_method_for_admin_users(self):
        self.client.login(username="admin_user", password="ytrewq123")
        new_name = "NewProjectName"
        new_description = "Description for new project"
        self.client.post(
            reverse("core:project-update", args=(self.project.id,)),
            data={"name": new_name, "description": new_description},
        )
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, new_name)
        self.assertEqual(self.project.description, new_description)


class ProjectDeleteViewTests(TestCase):
    def setUp(self):
        self.regular_user = get_user_model().objects.create_user(
            username="regular_user",
            password="ytrewq123",
        )
        self.admin = get_user_model().objects.create_superuser(
            username="admin_user",
            password="ytrewq123",
        )
        self.project = Project.objects.create(
            name="ProjectName", description="Description for ProjectName"
        )

    def test_redirect_for_not_logged_in_users(self):
        response = self.client.get(
            reverse("core:project-delete", args=(self.project.id,))
        )
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed("core/project_delete.html")

    def test_permission_denied_for_logged_in_regular_users(self):
        self.client.login(username="regular_user", password="ytrewq123")
        response = self.client.get(
            reverse("core:project-delete", args=(self.project.id,))
        )
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed("core/project_delete.html")

    def test_success_for_logged_admin_users(self):
        self.client.login(username="admin_user", password="ytrewq123")
        response = self.client.get(
            reverse("core:project-delete", args=(self.project.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("core/project_delete.html")

    def test_post_method_for_admin_users(self):
        self.client.login(username="admin_user", password="ytrewq123")
        response = self.client.post(
            reverse("core:project-delete", args=(self.project.pk,))
        )
        self.assertRedirects(response, reverse("core:project-list"))
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())
