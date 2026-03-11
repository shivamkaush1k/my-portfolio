from django.views.generic import TemplateView, ListView, DetailView
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
import os
from django.conf import settings
from .models import Skill, Certification, Stat, Project, Badge, Education


class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = Stat.objects.all()[:4]
        context['projects'] = Project.objects.filter(featured=True)[:3]
        context['skills'] = Skill.objects.all()[:8]
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = Stat.objects.all()
        context['skills'] = Skill.objects.all()
        context['certifications'] = Certification.objects.all()[:6]
        context['badges'] = Badge.objects.all()[:12]
        context['educations'] = Education.objects.all()
        
        # Enhanced certifications processing
        certifications = Certification.objects.all()
        enhanced_certs = []
        COLOR_MAP = {
            'primary': '0,123,255',
            'success': '40,167,69', 
            'info': '23,162,184',
            'warning': '255,193,7',
            'danger': '220,53,69',
            'secondary': '108,117,125'
        }
        
        for cert in certifications:
            cert_data = {
                'name': getattr(cert, 'name', 'N/A'),
                'provider': getattr(cert, 'provider', getattr(cert, 'provider_name', 'N/A')),
                'date_earned': getattr(cert, 'formatted_date_earned', 'N/A'),
                'expires': getattr(cert, 'formatted_expires', 'N/A'),
                'does_not_expire': getattr(cert, 'does_not_expire', False),
                'has_expiry': getattr(cert, 'has_expiry', True),
                'credential_id': getattr(cert, 'credential_id', ''),
                'badge_color': getattr(cert, 'badge_color', 'primary'),
                'color_rgb': getattr(cert, 'color_rgb', COLOR_MAP['primary']),
                'icon_class': getattr(cert, 'icon_class', 'fas fa-certificate'),
                'icon_url': getattr(cert, 'icon_url', ''),
                'verification_url': getattr(cert, 'verification_url', ''),
                'skills_gained': getattr(cert, 'skills_gained', '').split(',') if getattr(cert, 'skills_gained', '') else [],
            }
            enhanced_certs.append(cert_data)
        
        context['certifications'] = enhanced_certs
        return context


class ProjectsView(ListView):
    model = Project
    template_name = 'core/projects.html'
    context_object_name = 'projects'
    paginate_by = 6
    
    def get_queryset(self):
        return Project.objects.all().order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = Stat.objects.all()
        context['skills'] = Skill.objects.all()[:6]
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'core/project_detail.html'
    context_object_name = 'project'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Project, slug=slug)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context['related_projects'] = Project.objects.filter(
            category=project.category
        ).exclude(slug=project.slug)[:3]
        context['stats'] = Stat.objects.all()
        context['skills'] = Skill.objects.all()[:4]
        return context


# ✅ NEW: Class-based Resume Download View
class DownloadResumeView(View):
    def get(self, request):
        # Path to your resume (create media/resume/ folder first)
        resume_filename = 'Shivam_InternshalaResume (3).pdf'
        resume_path = os.path.join(settings.MEDIA_ROOT, 'resume', resume_filename)
        
        # Check media folder first
        if os.path.exists(resume_path):
            response = FileResponse(
                open(resume_path, 'rb'),
                content_type='application/pdf',
                as_attachment=True,
                filename=resume_filename
            )
            return response
        
        # Fallback: Check static folder
        static_resume_path = os.path.join(settings.STATIC_ROOT, 'resume', resume_filename)
        if os.path.exists(static_resume_path):
            response = FileResponse(
                open(static_resume_path, 'rb'),
                content_type='application/pdf',
                as_attachment=True,
                filename=resume_filename
            )
            return response
        
        # File not found
        return HttpResponse("Resume not found. Please upload it to media/resume/", status=404)
