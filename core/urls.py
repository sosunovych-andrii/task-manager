from django.urls import path

from core.views import (
    index,
    sign_up,
    ProjectListView,
    WorkerListView,
    TaskListView,
)

urlpatterns = [
    path("", index, name="index"),
    path("sign-up/", sign_up, name="sign-up"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("tasks/", TaskListView.as_view(), name="task-list")
]

app_name = "core"
