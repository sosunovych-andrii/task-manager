from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from core.forms.create_update_forms import TaskForm
from core.forms.search_forms import TaskSearchForm
from core.models import Task


class TaskListView(LoginRequiredMixin, generic.ListView):
    """Displays a paginated list of tasks with filtering support"""

    model = Task
    context_object_name = "task_list"
    template_name = "core/task_list.html"
    paginate_by = 4

    def get_queryset(self) -> QuerySet:
        queryset = (
            super().get_queryset().select_related("task_type", "project", "assignee")
        )
        form = TaskSearchForm(self.request.GET)
        if not form.is_valid():
            return queryset

        data = form.cleaned_data
        if data["assigned_to_me"] == "yes":
            queryset = queryset.filter(assignee=self.request.user)
        if data["assigned_to_me"] == "no":
            queryset = queryset.exclude(assignee=self.request.user)
        if data["created_by_me"] == "yes":
            queryset = queryset.filter(created_by=self.request.user)
        if data["created_by_me"] == "no":
            queryset = queryset.exclude(created_by=self.request.user)
        if data["status"] == "done":
            queryset = queryset.filter(is_completed=True)
        if data["status"] == "not_done":
            queryset = queryset.filter(is_completed=False)
        if data["name"]:
            queryset = queryset.filter(name__icontains=data["name"])
        if data["priority"]:
            queryset = queryset.filter(priority=data["priority"])
        if data["task_type"]:
            queryset = queryset.filter(task_type=data["task_type"])
        if data["project"]:
            queryset = queryset.filter(project=data["project"])

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        context["search_form"] = TaskSearchForm(
            initial={
                "name": self.request.GET.get("name", ""),
                "status": self.request.GET.get("status", ""),
                "assigned_to_me": self.request.GET.get("assigned_to_me", ""),
                "created_by_me": self.request.GET.get("created_by_me", ""),
                "priority": self.request.GET.get("priority", ""),
                "task_type": self.request.GET.get("task_type", ""),
                "project": self.request.GET.get("project", ""),
            }
        )

        return context


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    """Allows both users and admins to create tasks"""

    model = Task
    form_class = TaskForm
    context_object_name = "task"
    template_name = "core/task_form.html"
    success_url = reverse_lazy("core:task-list")

    def form_valid(self, form) -> HttpResponse:
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    """Allows admins or task creators info about tasks"""

    model = Task
    form_class = TaskForm
    context_object_name = "task"
    template_name = "core/task_form.html"
    success_url = reverse_lazy("core:task-list")

    def test_func(self) -> bool:
        return (
            self.request.user.is_superuser
            or self.get_object().created_by == self.request.user
        )


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """Allows admins or task creators to delete tasks"""

    model = Task
    context_object_name = "task"
    template_name = "core/task_delete.html"
    success_url = reverse_lazy("core:task-list")

    def test_func(self) -> bool:
        return (
            self.request.user.is_superuser
            or self.get_object().created_by == self.request.user
        )


@login_required
def task_mark_completed(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    """Marks a task as completed if user is an admin, assignee or creator"""

    task = get_object_or_404(Task, pk=pk)
    if (
        not request.user.is_superuser
        and task.assignee != request.user
        and task.created_by != request.user
    ):
        raise PermissionDenied
    if request.method == "POST":
        task.is_completed = True
        Task.objects.filter(pk=pk).update(is_completed=True)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
