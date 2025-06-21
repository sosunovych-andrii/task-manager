from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count, QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from core.forms import SignUpForm, MyProfileForm, WorkerForm
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
        return super().get_queryset().annotate(
            workers_count=Count("workers"),
            tasks_count=Count("tasks")
        )


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
        return super().get_queryset().select_related(
            "position", "project"
        ).annotate(tasks_count=Count("tasks"))


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
        return super().get_queryset().select_related(
            "task_type", "project", "worker"
        )


class MyProfileView(LoginRequiredMixin, generic.UpdateView):
    form_class = MyProfileForm
    template_name = "core/my_profile.html"
    success_url = reverse_lazy("core:my-profile")

    def get_object(self, **kwargs) -> User:
        return self.request.user


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerForm
    context_object_name = "worker"
    template_name = "core/worker_form.html"
    success_url = reverse_lazy("core:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    context_object_name = "worker"
    template_name = "core/worker_delete.html"
    success_url = reverse_lazy("core:worker-list")
