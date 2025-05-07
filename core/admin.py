from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from core.models import(
    Project,
    Position,
    Worker,
    TaskType,
    Task
)


admin.site.unregister(Group)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ("name", "description")


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "position",
        "project"
    )
    list_filter = (
        "is_superuser",
        "is_active",
        "is_staff",
        "position",
        "project"
    )
    list_select_related = ("position", "project")
    fieldsets = (
        (
            None,
            {
                "fields": ("username", "password")
            }
        ),
        (
            "Personal info",
            {
                "fields": ("first_name", "last_name", "email")
            }
        ),
        (
            "Permissions",
            {
            "fields": ("is_active", "is_staff", "is_superuser"),
            }
        ),
        (
            "Important dates",
            {
                "fields": ("last_login", "date_joined")
            }
        ),
        (
            "Additional info",
            {
                "fields": ("position", "project"),
            }
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": ("position", "project")
            }
        ),
    )
    autocomplete_fields = ("position", "project")


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "priority",
        "deadline",
        "is_completed",
        "task_type",
        "project",
        "worker"
    )
    list_filter = (
        "is_completed",
        "deadline",
        "priority",
        "task_type",
        "project",
        "worker"
    )
    list_select_related = ("task_type", "project", "worker")
    list_editable = ("deadline",)
    search_fields = ("name", "description")
    date_hierarchy = "deadline"
    autocomplete_fields = ("project", "worker")
