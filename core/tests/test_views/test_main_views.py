from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta


from core.models import Project, Worker, Task


class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.project = Project.objects.create(
            name="TestProject", description="Description for TestProject"
        )
        cls.task = Task.objects.create(
            name="TestTask",
            description="Description for TestTask",
            deadline=timezone.now() + timedelta(minutes=45),
            priority="LOW",
            is_completed=False,
            project=cls.project,
        )
        cls.worker = Worker.objects.create_user(username="user", password="ytrewq123")

    def test_index_page(self):
        response = self.client.get(reverse("core:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/index.html")

    def test_get_context_data(self):
        response = self.client.get(reverse("core:index"))
        self.assertEqual(response.context["num_projects"], 1)
        self.assertEqual(response.context["num_tasks"], 1)
        self.assertEqual(response.context["num_workers"], 1)
