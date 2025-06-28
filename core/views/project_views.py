from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, QuerySet
from django.urls import reverse_lazy
from django.views import generic

from core.forms.search_forms import ProjectSearchForm
from core.models import Project


class ProjectListView(LoginRequiredMixin, generic.ListView):
    """Displays a paginated list of projects with filtering support"""

    model = Project
    context_object_name = "project_list"
    template_name = "core/project_list.html"
    paginate_by = 8

    def get_queryset(self) -> QuerySet:
        queryset = (
            super()
            .get_queryset()
            .annotate(workers_count=Count("workers"), tasks_count=Count("tasks"))
        )
        form = ProjectSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = ProjectSearchForm(initial={"name": name})
        return context


class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    """Allows admins to create new projects"""

    model = Project
    fields = ("name", "description")
    context_object_name = "project"
    template_name = "core/project_form.html"
    success_url = reverse_lazy("core:project-list")

    def test_func(self) -> bool:
        return self.request.user.is_superuser


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    """Allows admins to update info about projects"""

    model = Project
    fields = ("name", "description")
    context_object_name = "project"
    template_name = "core/project_form.html"
    success_url = reverse_lazy("core:project-list")

    def test_func(self) -> bool:
        return self.request.user.is_superuser


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """Allows admins to delete projects"""

    model = Project
    context_object_name = "project"
    template_name = "core/project_delete.html"
    success_url = reverse_lazy("core:project-list")

    def test_func(self) -> bool:
        return self.request.user.is_superuser
