from django.urls import path

from core.views.main_views import index
from core.views.user_views import sign_up, MyProfileView
from core.views.project_views import (
    ProjectListView,
    ProjectUpdateView,
    ProjectDeleteView,
    ProjectCreateView
)
from core.views.task_views import (
    TaskListView,
    TaskUpdateView,
    TaskDeleteView,
    TaskCreateView,
    task_mark_completed
)
from core.views.worker_views import (
    WorkerListView,
    WorkerUpdateView,
    WorkerDeleteView,
    WorkerCreateView
)

urlpatterns = [
    path("", index, name="index"),
    path("sign-up/", sign_up, name="sign-up"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("my-profile/", MyProfileView.as_view(), name="my-profile"),
    path(
        "workers/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"
    ),
    path(
        "workers/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker-delete"
    ),
    path(
        "projects/<int:pk>/update/", ProjectUpdateView.as_view(), name="project-update"
    ),
    path(
        "projects/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project-delete"
    ),
    path(
        "tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"
    ),
    path(
        "tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"
    ),
    path(
        "workers/create/", WorkerCreateView.as_view(), name="worker-create"
    ),
    path(
        "projects/create/", ProjectCreateView.as_view(), name="project-create"
    ),
    path(
        "tasks/create/", TaskCreateView.as_view(), name="task-create"
    ),
    path(
        "tasks/<int:pk>/complete/", task_mark_completed, name="task-mark-completed"
    )
]

app_name = "core"
