from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('projects/', views.ProjectsView.as_view(), name='projects'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('download-resume/', views.DownloadResumeView.as_view(), name='download_resume'),  # ✅ Updated
]
