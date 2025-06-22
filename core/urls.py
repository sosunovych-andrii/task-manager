from django.urls import path

from core.views import (
    index,
    sign_up,
    ProjectListView,
    WorkerListView,
    TaskListView,
    MyProfileView,
    WorkerUpdateView,
    WorkerDeleteView,
    ProjectUpdateView,
    ProjectDeleteView,
    TaskUpdateView,
    TaskDeleteView,
    WorkerCreateView,
    ProjectCreateView,
    TaskCreateView
)


urlpatterns = [
    path("", index, name="index"),
    path("sign-up/", sign_up, name="sign-up"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("my-profile/", MyProfileView.as_view(), name="my-profile"),
    path("workers/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("workers/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker-delete"),
    path("projects/<int:pk>/update/", ProjectUpdateView.as_view(), name="project-update"),
    path("projects/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project-delete"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("projects/create/", ProjectCreateView.as_view(), name="project-create"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create")
]

app_name = "core"
