from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from core.forms.user_forms import SignUpForm, MyProfileForm


def sign_up(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """Handles user registration, authentication and login"""

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


class MyProfileView(LoginRequiredMixin, generic.UpdateView):
    """Allows users to view and update their profile information"""

    form_class = MyProfileForm
    template_name = "core/my_profile.html"
    success_url = reverse_lazy("core:my-profile")

    def get_object(self, **kwargs) -> User:
        return self.request.user
