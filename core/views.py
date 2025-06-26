from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Count, QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.utils import timezone

from core.forms import (
    SignUpForm,
    MyProfileForm,
    WorkerUpdateForm,
    TaskForm,
    WorkerCreationForm,
    ProjectSearchForm,
    WorkerSearchForm,
    TaskSearchForm
)
from core.models import Project, Task, Worker


def index(request: HttpRequest) -> HttpResponse:
    """View function for the home page of the site."""
    num_projects = Project.objects.count()
    num_tasks = Task.objects.count()
    num_workers = Worker.objects.count()

    context = {
        "num_projects": num_projects,
        "num_tasks": num_tasks,
        "num_workers": num_workers
    }

    return render(request, "core/index.html", context=context)


def sign_up(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """View function that handles user sign-up, authenticates and logs if the form is valid."""
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
    return render(request, "registration/sign_up.html", {"form": form})


class ProjectListView(LoginRequiredMixin, generic.ListView):
    """
    View class that displays a paginated list of projects
    with related workers and tasks count.
    """
    model = Project
    context_object_name = "project_list"
    template_name = "core/project_list.html"
    paginate_by = 8

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset().annotate(
            workers_count=Count("workers"),
            tasks_count=Count("tasks")
        )
        form = ProjectSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = ProjectSearchForm(
            initial={"name": name}
        )
        return context


class WorkerListView(LoginRequiredMixin, generic.ListView):
    """
    View class that displays a paginated list of workers
    with related position, project fields and tasks count
    """
    model = Worker
    context_object_name = "worker_list"
    template_name = "core/worker_list.html"
    paginate_by = 8

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset().select_related(
            "position", "project"
        ).annotate(tasks_count=Count("assigned_tasks"))

        form = WorkerSearchForm(self.request.GET)
        if not form.is_valid():
            return queryset

        data = form.cleaned_data
        if data["position"]:
            queryset = queryset.filter(position=data["position"])
        if data["project"]:
            queryset = queryset.filter(project=data["project"])
        if data["username"]:
            queryset = queryset.filter(username__icontains=data["username"])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["search_form"] = WorkerSearchForm(initial={
            "position": self.request.GET.get("position", ""),
            "project": self.request.GET.get("project", ""),
            "username": self.request.GET.get("username", ""),
        })
        return context


class TaskListView(LoginRequiredMixin, generic.ListView):
    """
    View class that displays a paginated list of tasks
    with related task_type, project and worker fields
    """
    model = Task
    context_object_name = "task_list"
    template_name = "core/task_list.html"
    paginate_by = 4

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset().select_related(
            "task_type", "project", "assignee"
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

    def get_context_data(self, *, object_list = ..., **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        context["search_form"] = TaskSearchForm(initial={
            "name": self.request.GET.get("name", ""),
            "status": self.request.GET.get("status", ""),
            "assigned_to_me": self.request.GET.get("assigned_to_me", ""),
            "created_by_me": self.request.GET.get("created_by_me", ""),
            "priority": self.request.GET.get("priority", ""),
            "task_type": self.request.GET.get("task_type", ""),
            "project": self.request.GET.get("project", ""),
        })

        return context


class MyProfileView(LoginRequiredMixin, generic.UpdateView):
    form_class = MyProfileForm
    template_name = "core/my_profile.html"
    success_url = reverse_lazy("core:my-profile")

    def get_object(self, **kwargs) -> User:
        return self.request.user


class WorkerUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    context_object_name = "worker"
    template_name = "core/worker_update_form.html"
    success_url = reverse_lazy("core:worker-list")

    def test_func(self) -> bool:
        return self.request.user.is_superuser


class WorkerDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Worker
    context_object_name = "worker"
    template_name = "core/worker_delete.html"
    success_url = reverse_lazy("core:worker-list")

    def test_func(self) -> bool:
        return self.request.user.is_superuser


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Project
    fields = ("name", "description")
    context_object_name = "project"
    template_name = "core/project_form.html"
    success_url = reverse_lazy("core:project-list")

    def test_func(self) -> bool:
        return self.request.user.is_superuser


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Project
    context_object_name = "project"
    template_name = "core/project_delete.html"
    success_url = reverse_lazy("core:project-list")

    def test_func(self) -> bool:
        return self.request.user.is_superuser


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    content_object_name = "task"
    template_name = "core/task_form.html"
    success_url = reverse_lazy("core:task-list")

    def test_func(self) -> bool:
        return (
                self.request.user.is_superuser or
                self.get_object().created_by == self.request.user
        )


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Task
    context_object_name = "task"
    template_name = "core/task_delete.html"
    success_url = reverse_lazy("core:task-list")

    def test_func(self) -> bool:
        return (
                self.request.user.is_superuser or
                self.get_object().created_by == self.request.user
        )


class WorkerCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    context_object_name = "worker"
    template_name = "core/worker_create_form.html"
    success_url = reverse_lazy("core:worker-list")

    def test_func(self) -> bool:
        return self.request.user.is_superuser


class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Project
    fields = ("name", "description")
    context_object_name = "project"
    template_name = "core/project_form.html"
    success_url = reverse_lazy("core:project-list")

    def test_func(self) -> bool:
        return self.request.user.is_superuser


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    content_object_name = "task"
    template_name = "core/task_form.html"
    success_url = reverse_lazy("core:task-list")

    def form_valid(self, form) -> HttpResponse:
        form.instance.created_by = self.request.user
        return super().form_valid(form)


@login_required
def task_mark_completed(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    task = get_object_or_404(Task, pk=pk)
    if (
        not request.user.is_superuser and
        task.assignee != request.user and
        task.created_by_id != request.user.id
    ):
        raise PermissionDenied
    if request.method == "POST":
        task.is_completed = True
        Task.objects.filter(pk=pk).update(is_completed=True)
        if task.assignee:
            task.assignee.completed_tasks += 1
            task.assignee.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
