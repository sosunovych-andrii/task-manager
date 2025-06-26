from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, Form
from django import forms

from core.models import Worker, Task, TaskType, Project, Position


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ["password1", "password2", "username"]:
            self.fields[field].help_text = ""

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("email",)


class MyProfileForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["position"].widget.attrs.update({
            "class": "select-field",
        })
        self.fields["project"].widget.attrs.update({
            "class": "select-field"
        })
        self.fields["username"].help_text = ""
        del self.fields["password"]

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = (
            "username", "position", "project",
            "first_name", "last_name", "email"
        )


class WorkerUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["position"].widget.attrs.update({
            "class": "select-field",
        })
        self.fields["project"].widget.attrs.update({
            "class": "select-field"
        })
        self.fields["username"].help_text = ""

    class Meta:
        model = Worker
        fields = (
            "username", "position", "project",
            "first_name", "last_name", "email"
        )


class WorkerCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["position"].widget.attrs.update({
            "class": "select-field",
        })
        self.fields["project"].widget.attrs.update({
            "class": "select-field"
        })
        for field in ["password1", "password2", "username"]:
            self.fields[field].help_text = ""

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = (
            "username", "position",
            "project", "first_name",
            "last_name", "email",
            "password1", "password2"
        )


class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["project"].required = True

    class Meta:
        model = Task
        fields = (
        "name", "deadline",
        "priority", "task_type",
        "project", "assignee",
        "description"
        )
        widgets = {
            "deadline": forms.DateTimeInput(
                attrs={"placeholder": "YYYY-MM-DD HH:MM"}
            ),
            "priority": forms.Select(attrs={"class": "select-field"}),
            "task_type": forms.Select(attrs={"class": "select-field"}),
            "project": forms.Select(attrs={"class": "select-field"}),
            "assignee": forms.Select(attrs={"class": "select-field"})
        }


class ProjectSearchForm(Form):
    name = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Entet the project name"}
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
        choices=[("", "----------"), ("yes", "Yes"), ("no", "No")],
        required=False,
        widget=forms.Select(attrs={"class": "select-field"}),
        label="Assigned to me"
    )
    status = forms.ChoiceField(
        choices=[("", "----------"), ("done", "Completed"), ("not_done", "Not completed")],
        required=False,
        widget=forms.Select(attrs={"class": "select-field"}),
        label="Status"
    )
    created_by_me = forms.ChoiceField(
        choices=[("", "----------"), ("yes", "Yes"), ("no", "No")],
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
