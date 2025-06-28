from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in ["password1", "password2", "username"]:
            self.fields[field].help_text = ""

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("email",)


class MyProfileForm(UserChangeForm):
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

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = (
            "username", "position", "project",
            "first_name", "last_name", "email"
        )
