from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from task_manager import settings


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    completed_tasks = models.PositiveIntegerField(default=0)

    position = models.ForeignKey(
        to=Position,
        on_delete=models.SET_NULL,
        null=True,
        related_name="workers",
        blank=True
    )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.SET_NULL,
        null=True,
        related_name="workers",
        blank=True
    )

    class Meta:
        ordering = ["username"]


class TaskType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High")
    ]
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES
    )
    is_completed = models.BooleanField(default=False)

    task_type = models.ForeignKey(
        to=TaskType,
        on_delete=models.SET_NULL,
        null=True,
        related_name="tasks",
        blank=True
    )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name="tasks",
        blank=True
    )
    worker = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="tasks",
        blank=True
    )

    class Meta:
        ordering = ["deadline"]

    def clean(self) -> None:
        super().clean()
        if self.deadline and self.deadline < timezone.now() + timedelta(minutes=30):
            raise ValidationError(
                "Deadline must be at least 30 minutes from now."
            )

    def __str__(self) -> str:
        return self.name
