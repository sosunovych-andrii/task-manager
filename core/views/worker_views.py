from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import QuerySet, Count
from django.urls import reverse_lazy
from django.views import generic

from core.forms.create_update_forms import WorkerUpdateForm, WorkerCreationForm
from core.forms.search_forms import WorkerSearchForm
from core.models import Worker


class WorkerListView(LoginRequiredMixin, generic.ListView):
    """Displays a paginated list of workers with filtering support"""

    model = Worker
    context_object_name = "worker_list"
    template_name = "core/worker_list.html"
    paginate_by = 8

    def get_queryset(self) -> QuerySet:
        queryset = (
            super()
            .get_queryset()
            .select_related("position", "project")
            .annotate(tasks_count=Count("assigned_tasks"))
        )

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
        context["search_form"] = WorkerSearchForm(
            initial={
                "position": self.request.GET.get("position", ""),
                "project": self.request.GET.get("project", ""),
                "username": self.request.GET.get("username", ""),
            }
        )
        return context


class WorkerUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    """Allows admins to update info about workers"""

    model = Worker
    form_class = WorkerUpdateForm
    context_object_name = "worker"
    template_name = "core/worker_update_form.html"
    success_url = reverse_lazy("core:worker-list")

    def test_func(self) -> bool:
        return self.request.user.is_superuser


class WorkerDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """Allows admins to delete workers"""
    model = Worker
    context_object_name = "worker"
    template_name = "core/worker_delete.html"
    success_url = reverse_lazy("core:worker-list")

    def test_func(self) -> bool:
        return self.request.user.is_superuser


class WorkerCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    """Allows admins to create new workers"""

    model = Worker
    form_class = WorkerCreationForm
    context_object_name = "worker"
    template_name = "core/worker_create_form.html"
    success_url = reverse_lazy("core:worker-list")

    def test_func(self) -> bool:
        return self.request.user.is_superuser
