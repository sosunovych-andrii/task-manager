from django.urls import path

from core.views import (
    index,
    sign_up,
)

urlpatterns = [
    path("", index, name="index"),
    path("sign-up/", sign_up, name="sign-up")
]

app_name = "core"
