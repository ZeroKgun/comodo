from django.urls import path

from .views import CodeProfileAPI

urlpatterns = [
    path("code_profile/", CodeProfileAPI.as_view(), name="code_profile_api")
]

