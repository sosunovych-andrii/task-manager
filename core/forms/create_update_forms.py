from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django import forms

from core.models import Worker, Task


class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs) -> None:
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


class WorkerCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs) -> None:
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


class WorkerUpdateForm(UserChangeForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["position"].widget.attrs.update({
            "class": "select-field",
        })
        self.fields["project"].widget.attrs.update({
            "class": "select-field"
        })
        self.fields["username"].help_text = ""
        del self.fields["password"]

    class Meta:
        model = Worker
        fields = (
            "username", "position", "project",
            "first_name", "last_name", "email"
        )
