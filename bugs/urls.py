from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("bug/<int:bug_id>/", views.bug_detail, name="bug_detail"),
    path(
        "bug/<int:bug_id>/status/",
        views.update_bug_status,
        name="update_bug_status",
    ),
]
