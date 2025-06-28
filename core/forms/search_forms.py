from django.forms import Form
from django import forms

from core.models import Task, TaskType, Project, Position


class ProjectSearchForm(Form):
    name = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter the project name"}
        )
    )


class WorkerSearchForm(Form):
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "select-field"}),
        label="Position"
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "select-field"}),
        label="Project"
    )
    username = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter the username"}
        )
    )


class TaskSearchForm(Form):
    assigned_to_me = forms.ChoiceField(
        choices=[
            ("", "----------"),
            ("yes", "Yes"),
            ("no", "No")
        ],
        required=False,
        widget=forms.Select(attrs={"class": "select-field"}),
        label="Assigned to me"
    )
    status = forms.ChoiceField(
        choices=[
            ("", "----------"),
            ("done", "Completed"),
            ("not_done", "Not completed")
        ],
        required=False,
        widget=forms.Select(attrs={"class": "select-field"}),
        label="Status"
    )
    created_by_me = forms.ChoiceField(
        choices=[
            ("", "----------"),
            ("yes", "Yes"),
            ("no", "No")
        ],
        required=False,
        widget=forms.Select(attrs={"class": "select-field"}),
        label="Created by me"
    )
    priority = forms.ChoiceField(
        choices=[("", "----------")] + Task.PRIORITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "select-field"}),
        label="Priority"
    )
    task_type = forms.ModelChoiceField(
        queryset=TaskType.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "select-field"}),
        label="Task Type"
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "select-field"}),
        label="Project"
    )
    name = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter the task name"
            }
        )
    )
