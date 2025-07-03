from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from core.models import TaskType, Position, Task, Project
from core.views.task_views import TaskListView


class TaskListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.project = Project.objects.create(
            name="ProjectName",
            description="Description for project",
        )
        cls.task_type = TaskType.objects.create(name="TaskType")
        cls.position = Position.objects.create(name="PositionName")
        cls.users = []
        for i in range(10):
            user = get_user_model().objects.create_user(
                username=f"user{i}",
                password="ytrewq123",
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
                task_type=cls.task_type,
                assignee=cls.users[i],
                created_by=cls.users[i],
                is_completed=(i % 2 == 0),
            )
            cls.tasks.append(task)

    def test_redirect_for_not_logged_in_users(self):
        response = self.client.get(reverse("core:task-list"))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, "core/task_list.html")

    def test_success_for_logged_in_users(self):
        self.client.login(username="user0", password="ytrewq123")
        response = self.client.get(reverse("core:task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/task_list.html")

    def test_list_pagination(self):
        self.client.login(username="user0", password="ytrewq123")
        response = self.client.get(reverse("core:task-list") + "?page=1")
        self.assertEqual(len(response.context["task_list"]), 4)
        response = self.client.get(reverse("core:task-list") + "?page=3")
        self.assertEqual(len(response.context["task_list"]), 2)

    def test_get_queryset_with_valid_form(self):
        request = RequestFactory().get(
            reverse("core:task-list"),
            data={
                "assigned_to_me": "yes",
                "created_by_me": "yes",
                "status": "done",
                "name": "TaskName0",
                "priority": "LOW",
                "task_type": self.task_type.pk,
                "project": self.project.pk,
            },
        )
        request.user = self.users[0]
        view = TaskListView()
        view.request = request
        queryset = view.get_queryset().values("task_type", "project", "assignee")
        expected_queryset = (
            Task.objects.select_related("task_type", "project", "assignee")
            .filter(
                assignee=self.users[0],
                created_by=self.users[0],
                is_completed=True,
                name__icontains="TaskName0",
                priority="LOW",
                task_type=self.task_type,
                project=self.project,
            )
            .values("task_type", "project", "assignee")
        )
        self.assertEqual(list(queryset.values()), list(expected_queryset.values()))

    def test_get_queryset_with_invalid_form(self):
        self.client.login(username="user0", password="ytrewq123")
        request = RequestFactory().get(
            reverse("core:task-list"), data={"priority": "INVALID"}
        )
        request.user = self.users[0]
        view = TaskListView()
        view.request = request
        queryset = view.get_queryset().values("task_type", "project", "assignee")
        expected_queryset = (
            Task.objects.select_related("task_type", "project", "assignee")
        ).values("task_type", "project", "assignee")
        self.assertEqual(list(queryset.values()), list(expected_queryset.values()))

    def test_get_context_data(self):
        request = RequestFactory().get(
            reverse("core:task-list"),
            data={
                "assigned_to_me": "yes",
                "created_by_me": "yes",
                "status": "done",
                "name": "TaskName0",
                "priority": "LOW",
                "task_type": self.task_type,
                "project": self.project,
            },
        )
        request.user = self.users[0]
        response = TaskListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("now", response.context_data)
        self.assertIn("search_form", response.context_data)
        self.assertEqual(
            response.context_data["search_form"].initial["name"], "TaskName0"
        )
        self.assertEqual(
            response.context_data["search_form"].initial["assigned_to_me"], "yes"
        )
        self.assertEqual(
            response.context_data["search_form"].initial["created_by_me"], "yes"
        )
        self.assertEqual(response.context_data["search_form"].initial["status"], "done")
        self.assertEqual(
            response.context_data["search_form"].initial["priority"], "LOW"
        )
        self.assertEqual(
            response.context_data["search_form"].initial["task_type"],
            str(self.task_type),
        )
        self.assertEqual(
            response.context_data["search_form"].initial["project"], str(self.project)
        )


class TaskCreateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="user",
            password="ytrewq123",
        )
        cls.project = Project.objects.create(
            name="ProjectName",
            description="Description for project",
        )

    def test_redirect_for_not_logged_in_users(self):
        response = self.client.get(reverse("core:task-create"))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed("core/task_form.html")

    def test_success_for_logged_in_users(self):
        self.client.login(username="user", password="ytrewq123")
        response = self.client.get(reverse("core:task-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("core/task_form.html")

    def test_post_method(self):
        self.client.login(username="user", password="ytrewq123")
        response = self.client.post(
            reverse("core:task-create"),
            data={
                "name": "NewTask",
                "description": "Description for new task",
                "deadline": timezone.now() + timedelta(minutes=45),
                "priority": "LOW",
                "project": self.project.id,
                "assignee": self.user.id,
            },
        )
        task = Task.objects.get(name="NewTask")
        self.assertEqual(task.created_by, self.user)
        self.assertTrue(Task.objects.filter(name="NewTask").exists())
        self.assertRedirects(response, reverse("core:task-list"))


class TaskUpdateViewTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username="admin_user", password="ytrewq123"
        )
        self.regular_user = get_user_model().objects.create_user(
            username="regular_user", password="ytrewq123"
        )
        self.creator = get_user_model().objects.create_user(
            username="creator", password="ytrewq123"
        )
        self.project = Project.objects.create(
            name="TestProject", description="Description for project"
        )
        self.task = Task.objects.create(
            name="Task1",
            description="Description",
            deadline=timezone.now() + timedelta(minutes=45),
            priority="HIGH",
            project=self.project,
            created_by=self.creator,
        )

    def test_redirect_for_not_logged_in_users(self):
        response = self.client.get(reverse("core:task-create"))
        self.assertEqual(response.status_code, 302)

    def test_permission_denied_for_logged_in_regular_users(self):
        self.client.login(username="regular_user", password="ytrewq123")
        response = self.client.get(reverse("core:task-update", args=(self.task.id,)))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed("core/task_form.html")

    def test_success_for_logged_in_admin_users(self):
        self.client.login(username="admin_user", password="ytrewq123")
        response = self.client.get(reverse("core:task-update", args=(self.task.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("core/task_form.html")

    def test_success_for_logged_in_creators(self):
        self.client.login(username="creator", password="ytrewq123")
        response = self.client.get(reverse("core:task-update", args=(self.task.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("core/task_form.html")

    def test_post_method_for_admin_users(self):
        self.client.login(username="admin_user", password="ytrewq123")
        new_task_name = "NewName"
        new_description = "New description"
        self.client.post(
            reverse("core:task-update", args=(self.task.id,)),
            data={
                "name": new_task_name,
                "project": self.task.project.id,
                "description": new_description,
                "priority": self.task.priority,
                "deadline": self.task.deadline,
            },
        )
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, new_task_name)
        self.assertEqual(self.task.description, new_description)

    def test_post_method_for_creators(self):
        self.client.login(username="creator", password="ytrewq123")
        new_priority = "MEDIUM"
        new_deadline = timezone.now() + timedelta(hours=4)
        self.client.post(
            reverse("core:task-update", args=(self.task.id,)),
            data={
                "name": self.task.name,
                "project": self.task.project.id,
                "description": self.task.description,
                "priority": new_priority,
                "deadline": new_deadline,
            },
        )
        self.task.refresh_from_db()
        self.assertEqual(self.task.priority, new_priority)
        self.assertEqual(self.task.deadline, new_deadline)


class TaskDeleteViewTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="TestProject", description="Description for project"
        )
        self.admin = get_user_model().objects.create_superuser(
            username="admin_user", password="ytrewq123"
        )
        self.regular_user = get_user_model().objects.create_user(
            username="regular_user", password="ytrewq123"
        )
        self.creator = get_user_model().objects.create_user(
            username="creator", password="ytrewq123"
        )
        self.task = Task.objects.create(
            name="Task1",
            description="Description",
            deadline=timezone.now() + timedelta(minutes=45),
            priority="HIGH",
            project=self.project,
            created_by=self.creator,
        )

    def test_redirect_for_not_logged_in_users(self):
        response = self.client.get(reverse("core:task-delete", args=(self.task.id,)))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, "core/task_delete.html")

    def test_permission_denied_for_logged_in_regular_users(self):
        self.client.login(username="regular_user", password="ytrewq123")
        response = self.client.get(reverse("core:worker-delete", args=(self.task.id,)))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, "core/task_delete.html")

    def test_success_for_logged_admin_users(self):
        self.client.login(username="admin_user", password="ytrewq123")
        response = self.client.get(reverse("core:task-delete", args=(self.task.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/task_delete.html")

    def test_post_method_for_admin_users(self):
        self.client.login(username="admin_user", password="ytrewq123")
        response = self.client.post(reverse("core:task-delete", args=(self.task.id,)))
        self.assertRedirects(response, reverse("core:task-list"))
        self.assertFalse(Task.objects.filter(pk=self.task.id).exists())

    def test_post_method_for_creators(self):
        self.client.login(username="creator", password="ytrewq123")
        response = self.client.post(reverse("core:task-delete", args=(self.task.id,)))
        self.assertRedirects(response, reverse("core:task-list"))
        self.assertFalse(Task.objects.filter(pk=self.task.id).exists())


class TaskMarkCompletedViewTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username="admin", password="ytrewq123"
        )
        self.creator = get_user_model().objects.create_user(
            username="creator", password="ytrewq123"
        )
        self.assignee = get_user_model().objects.create_user(
            username="assignee", password="ytrewq123"
        )
        self.regular_user = get_user_model().objects.create_user(
            username="regular_user", password="ytrewq123"
        )
        self.project = Project.objects.create(
            name="TestProject", description="Description for project"
        )
        self.task = Task.objects.create(
            name="Task1",
            description="Test task",
            deadline=timezone.now() + timedelta(minutes=45),
            priority="HIGH",
            project=self.project,
            assignee=self.assignee,
            created_by=self.creator,
        )

    def test_redirect_for_not_logged_in_users(self):
        response = self.client.post(
            reverse("core:task-mark-completed", args=(self.task.id,))
        )
        self.assertEqual(response.status_code, 302)

    def test_permission_denied_for_regular_users(self):
        self.client.login(username="regular_user", password="ytrewq123")
        response = self.client.post(
            reverse("core:task-mark-completed", args=(self.task.id,))
        )
        self.assertEqual(response.status_code, 403)
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_completed)

    def test_admins_can_mark_completed(self):
        self.client.login(username="admin", password="ytrewq123")
        response = self.client.post(
            reverse("core:task-mark-completed", args=(self.task.id,))
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)

    def test_assignees_can_mark_completed(self):
        self.client.login(username="assignee", password="ytrewq123")
        response = self.client.post(
            reverse("core:task-mark-completed", args=(self.task.id,))
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)

    def test_creators_can_mark_completed(self):
        self.client.login(username="creator", password="ytrewq123")
        response = self.client.post(
            reverse("core:task-mark-completed", args=(self.task.id,))
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)

    def test_get_method_does_not_mark_completed(self):
        self.client.login(username="assignee", password="ytrewq123")
        response = self.client.get(
            reverse("core:task-mark-completed", args=(self.task.id,))
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_completed)
