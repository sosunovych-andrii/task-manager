from django.urls import path

from core.views import (
    index,
    sign_up,
    ProjectListView,
)

urlpatterns = [
    path("", index, name="index"),
    path("sign-up/", sign_up, name="sign-up"),
    path("projects/", ProjectListView.as_view(), name="project-list")
]

app_name = "core"
