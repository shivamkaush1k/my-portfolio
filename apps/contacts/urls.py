from django.urls import path
from . import views

app_name = "contacts"
urlpatterns = [
    path("", views.contact_view, name="contacts"),
    path('linkedin/', views.contact_linkedin, name='contact_linkedin'),
    path('github/', views.contact_github, name='contact_github'),
    path('instagram/', views.contact_instagram, name='contact_instagram'),
]
