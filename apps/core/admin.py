from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Skill, Certification, Stat, Project, Badge, Education

# =====================================================
# SITE CONFIGURATION
admin.site.site_header = "Shivam Portfolio Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Welcome to Shivam's Portfolio Dashboard"

# =====================================================
# EDUCATION ADMIN - CGPA SUPPORT ✅
@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'duration', 'percentage_or_cgpa_display', 'icon']
    list_filter = ['degree']
    search_fields = ['degree', 'institution']
    ordering = ['-duration']
    
    fieldsets = (
        ('📚 Education Details', {
            'fields': ('degree', 'institution', 'duration', 'percentage_or_cgpa', 'icon')
        }),
        ('📝 Description', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
    )
    
    def percentage_or_cgpa_display(self, obj):
        if obj.percentage_or_cgpa:
            if obj.percentage_or_cgpa >= 8:
                return f"{obj.percentage_or_cgpa} ⭐ CGPA"
            return f"{obj.percentage_or_cgpa}%"
        return "N/A"
    percentage_or_cgpa_display.short_description = "Score"

# =====================================================
# SKILL ADMIN - PERFECT ✅
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'proficiency', 'color_class', 'icon_class')
    list_editable = ('proficiency',)
    list_filter = ('color_class',)
    search_fields = ('name',)

# =====================================================
# CERTIFICATION ADMIN - ENHANCED ✅
@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider_name', 'date_earned', 'does_not_expire_display', 'badge_color']
    list_filter = ['badge_color', 'does_not_expire', 'date_earned']
    search_fields = ['name', 'credential_id', 'provider']
    readonly_fields = ['provider_name']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'cert', 'badge_color')
        }),
        ('Details', {
            'fields': ('provider', 'date_earned', 'expires', 'does_not_expire', 'credential_id')
        }),
        ('Display', {
            'fields': ('color_rgb', 'icon_class', 'icon_url', 'verification_url')
        }),
    )
    
    def does_not_expire_display(self, obj):
        return "✅ Lifetime" if obj.does_not_expire else "📅 Expires"
    does_not_expire_display.short_description = "Expiry Status"

# =====================================================
# STAT ADMIN - PERFECT ✅
@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'color_class')
    list_editable = ('value', 'color_class')

# =====================================================
# PROJECT ADMIN - PRODUCTION READY ✅
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'featured', 'created_at', 'has_github', 'has_live']
    list_filter = ['category', 'featured', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['featured']
    
    fieldsets = (
        ('⭐ Featured', {
            'fields': ('title', 'slug', 'category', 'featured'),
            'classes': ('collapse-open',)
        }),
        ('📝 Content', {
            'fields': ('description', 'short_description', 'image'),
            'classes': ('wide',)
        }),
        ('🔗 Links', {
            'fields': ('github_url', 'live_url'),
            'classes': ('collapse',)
        }),
        ('💻 Tech Stack', {
            'fields': ('technologies',),
            'description': 'Comma-separated: <code>Django, PostgreSQL, React, Tailwind</code>',
            'classes': ('collapse',)
        }),
    )
    
    def has_github(self, obj):
        return '✅' if obj.github_url else '❌'
    has_github.short_description = 'GitHub'
    has_github.admin_order_field = 'github_url'
    
    def has_live(self, obj):
        return '✅' if obj.live_url else '❌'
    has_live.short_description = 'Live Demo'
    has_live.admin_order_field = 'live_url'

# =====================================================
# BADGE ADMIN - ENHANCED ✅
@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'skill', 'issuer', 'date_earned', 'has_image']
    list_filter = ['skill', 'issuer', 'date_earned']
    search_fields = ['name', 'skill', 'issuer']
    readonly_fields = ['image_preview', 'created_at']
    
    fieldsets = (
        ('🏆 Badge Info', {
            'fields': ('name', 'skill', 'issuer')
        }),
        ('📸 Image', {
            'fields': ('image', 'image_preview'),
        }),
        ('🔗 Verification', {
            'fields': ('verification_url', 'date_earned'),
            'classes': ('collapse',)
        }),
    )
    
    def has_image(self, obj):
        return '✅' if obj.image else '❌'
    has_image.short_description = 'Image'
    
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" style="object-fit: contain;" />')
        return "No image"
    image_preview.short_description = "Image Preview"
