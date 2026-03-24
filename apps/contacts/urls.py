from django.urls import path
from . import views

app_name = "contacts"

urlpatterns = [
    path("", views.contact_view, name="contact"),
    path("linkedin/", views.contact_linkedin, name="linkedin_redirect"),
    path("github/", views.contact_github, name="github_redirect"),
    path("instagram/", views.contact_instagram, name="instagram_redirect"),
    path("x/", views.contact_x, name="x_redirect"),
]
