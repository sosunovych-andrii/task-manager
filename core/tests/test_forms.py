from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from core.forms.user_forms import MyProfileForm, SignUpForm
from core.models import Position, Project, Worker, TaskType
from core.forms.create_update_forms import (
    TaskForm,
    WorkerUpdateForm,
    WorkerCreationForm,
)


class MyProfileFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(name="TestPosition")
        cls.project = Project.objects.create(
            name="TestProject", description="Description for TestProject"
        )
        cls.worker = Worker.objects.create_user(
            username="user",
            password="ytrewq123",
            position=cls.position,
            project=cls.project,
            first_name="John",
            last_name="Doe",
        )
        cls.form = MyProfileForm(instance=cls.worker)

    def test_my_profile_select_fields_have_custom_class(self):
        self.assertIn(
            "select-field", self.form.fields["position"].widget.attrs.get("class", "")
        )
        self.assertIn(
            "select-field", self.form.fields["project"].widget.attrs.get("class", "")
        )

    def test_my_profile_username_help_text_removed(self):
        self.assertEqual(self.form.fields["username"].help_text, "")

    def test_my_profile_password_field_removed(self):
        self.assertNotIn("password", self.form.fields)


class SignUpFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form_data = {
            "username": "user",
            "email": "example@gmail.com",
            "password1": "ytrewq123",
            "password2": "ytrewq123",
        }
        cls.form = SignUpForm(data=cls.form_data)

    def test_sign_up_is_valid_form(self):
        self.assertTrue(self.form.is_valid())

    def test_sign_up_fields_help_text_removed(self):
        for field in ["password1", "password2", "username"]:
            self.assertEqual(self.form.fields[field].help_text, "")


class CreateUpdateFormSetup(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(name="TestPosition")
        cls.project = Project.objects.create(
            name="TestProject", description="Description for TestProject"
        )
        cls.task_type = TaskType.objects.create(name="TaskType")
        cls.worker = Worker.objects.create_user(
            username="user",
            password="ytrewq123",
            first_name="John",
            last_name="Doe",
            email="example@gmail.com",
            position=cls.position,
            project=cls.project,
        )


class TaskFormTest(CreateUpdateFormSetup):
    def test_task_form_valid(self):
        form_data = {
            "name": "Fix issue",
            "description": "Fix a major bug",
            "deadline": timezone.now() + timedelta(hours=1),
            "priority": "HIGH",
            "is_completed": False,
            "task_type": self.task_type,
            "project": self.project,
            "assignee": self.worker,
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_project_field_is_required(self):
        form_data = {
            "name": "Task without project",
            "description": "Description for task",
            "deadline": timezone.now() + timedelta(hours=1),
            "priority": "MEDIUM",
            "is_completed": False,
            "task_type": self.task_type,
            "assignee": self.worker,
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("project", form.errors)

    def test_task_deadline_placeholder(self):
        form = TaskForm()
        self.assertIn(
            "YYYY-MM-DD HH:MM",
            form.fields["deadline"].widget.attrs.get("placeholder", ""),
        )

    def test_select_fields_have_class(self):
        form = TaskForm()
        for field in ["priority", "task_type", "project", "assignee"]:
            self.assertIn(
                "select-field", form.fields[field].widget.attrs.get("class", "")
            )


class WorkerCreationFormTest(CreateUpdateFormSetup):
    def test_worker_creation_form_valid(self):
        form_data = {
            "username": "user2",
            "first_name": self.worker.first_name,
            "last_name": self.worker.last_name,
            "email": self.worker.email,
            "password1": self.worker.password,
            "password2": self.worker.password,
            "position": self.position.id,
            "project": self.project.id,
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_worker_select_fields_have_class(self):
        form = WorkerCreationForm()
        self.assertIn(
            "select-field", form.fields["position"].widget.attrs.get("class", "")
        )
        self.assertIn(
            "select-field", form.fields["project"].widget.attrs.get("class", "")
        )

    def test_worker_help_texts_removed(self):
        form = WorkerCreationForm()
        for field in ["username", "password1", "password2"]:
            self.assertEqual(form.fields[field].help_text, "")


class WorkerUpdateFormTest(CreateUpdateFormSetup):
    def test_worker_update_form_valid(self):
        form_data = {
            "username": self.worker.username,
            "first_name": "andrii",
            "last_name": "shevchenko",
            "email": "new_email@gmail.com",
            "position": self.position.id,
            "project": self.project.id,
        }
        form = WorkerUpdateForm(data=form_data, instance=self.worker)
        self.assertTrue(form.is_valid())

    def test_worker_select_fields_have_class(self):
        form = WorkerUpdateForm(instance=self.worker)
        self.assertIn(
            "select-field", form.fields["position"].widget.attrs.get("class", "")
        )
        self.assertIn(
            "select-field", form.fields["project"].widget.attrs.get("class", "")
        )

    def test_worker_username_help_text_removed(self):
        form = WorkerUpdateForm(instance=self.worker)
        self.assertEqual(form.fields["username"].help_text, "")

    def test_worker_password_field_removed(self):
        form = WorkerUpdateForm(instance=self.worker)
        self.assertNotIn("password", form.fields)
