from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django import forms

from core.models import Worker, Task


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
    class Meta:
        model = Task
        fields = (
        "name", "deadline",
        "priority", "task_type",
        "project", "worker",
        "description"
        )
        widgets = {
            "priority": forms.Select(attrs={"class": "select-field"}),
            "task_type": forms.Select(attrs={"class": "select-field"}),
            "project": forms.Select(attrs={"class": "select-field"}),
            "worker": forms.Select(attrs={"class": "select-field"})
        }
