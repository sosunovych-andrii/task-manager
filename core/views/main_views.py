from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from core.models import Project, Task, Worker


def index(request: HttpRequest) -> HttpResponse:
    """Renders the home page with counts of projects, tasks and workers"""
    num_projects = Project.objects.count()
    num_tasks = Task.objects.count()
    num_workers = Worker.objects.count()

    context = {
        "num_projects": num_projects,
        "num_tasks": num_tasks,
        "num_workers": num_workers
    }

    return render(request, "core/index.html", context=context)
