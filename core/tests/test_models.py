from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from core.models import Project, Position, Worker, TaskType, Task


class ProjectModelTests(TestCase):
    def test_project_str(self):
        project = Project.objects.create(
            name="TestProject", description="Description for TestProject"
        )
        self.assertEqual(str(project), "TestProject")


class PositionModelTests(TestCase):
    def test_position_str(self):
        position = Position.objects.create(name="TestProject")
        self.assertEqual(str(position), "TestProject")


class WorkerModelTests(TestCase):
    def test_worker_clean_with_valid_data(self):
        worker = Worker(
            username="user",
            first_name="John",
            last_name="Doe",
        )
        worker.set_password("ytrewq123")
        worker.full_clean()

    def test_worker_clean_with_invalid_first_name(self):
        worker = Worker(
            username="user",
            first_name="J0hn",
            last_name="Doe",
        )
        worker.set_password("ytrewq123")
        with self.assertRaises(ValidationError):
            worker.full_clean()

    def test_worker_clean_with_invalid_last_name(self):
        worker = Worker(
            username="user",
            first_name="John",
            last_name="D0e",
        )
        worker.set_password("ytrewq123")
        with self.assertRaises(ValidationError):
            worker.full_clean()

    def test_worker_clean_with_invalid_name(self):
        worker = Worker(
            username="user",
            first_name="J0hn#$!",
            last_name="D0e*&?",
        )
        worker.set_password("ytrewq123")
        with self.assertRaises(ValidationError):
            worker.full_clean()

    def test_worker_save_with_valid_data(self):
        worker = Worker(
            username="user",
            first_name="John",
            last_name="Doe",
        )
        worker.set_password("ytrewq123")
        worker.save()
        self.assertIsNotNone(worker.id)

    def test_worker_save_with_invalid_first_name(self):
        worker = Worker(username="user", first_name="J0hn__", last_name="Doe")
        worker.set_password("ytrewq123")
        with self.assertRaises(ValidationError):
            worker.save()

    def test_worker_save_with_invalid_last_name(self):
        worker = Worker(username="user", first_name="John", last_name="Doe_1#")
        worker.set_password("ytrewq123")
        with self.assertRaises(ValidationError):
            worker.save()

    def test_worker_save_with_invalid_data(self):
        worker = Worker(username="user", first_name="J0hn[1]", last_name="Doe/")
        worker.set_password("ytrewq123")
        with self.assertRaises(ValidationError):
            worker.save()


class TaskTypeModelTests(TestCase):
    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="TestTaskType")
        self.assertEqual(str(task_type), "TestTaskType")


class TaskModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.project = Project.objects.create(
            name="TestProject", description="Description for TestProject"
        )
        cls.task = Task(
            name="TestTask",
            description="Description for TestTask",
            deadline=timezone.now() + timedelta(minutes=45),
            priority="LOW",
            is_completed=False,
            project=cls.project,
        )

    def test_task_clean_with_valid_deadline(self):
        self.task.deadline = timezone.now() + timedelta(hours=1)
        self.task.full_clean()

    def test_task_clean_with_invalid_deadline(self):
        self.task.deadline = timezone.now()
        with self.assertRaises(ValidationError):
            self.task.full_clean()

    def test_task_save_with_valid_deadline(self):
        self.task.deadline = timezone.now() + timedelta(minutes=45)
        self.task.save()
        self.assertIsNotNone(self.task.id)

    def test_task_save_with_invalid_deadline(self):
        self.task.deadline = timezone.now() + timedelta(minutes=25)
        with self.assertRaises(ValidationError):
            self.task.save()

    def test_task_str(self):
        self.assertEqual(str(self.task), "TestTask")
