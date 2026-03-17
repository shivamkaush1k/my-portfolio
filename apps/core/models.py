from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon_class = models.CharField(max_length=50, default="fas fa-star")
    proficiency = models.PositiveIntegerField(help_text="0-100")
    color_class = models.CharField(max_length=50, help_text="primary, success, info, warning")

    class Meta:
        ordering = ['-proficiency', 'name']
    
    def __str__(self):
        return self.name
class Certification(models.Model):
    name = models.CharField(max_length=200, unique=True)
    cert = models.CharField(max_length=200, blank=True)
    badge_color = models.CharField(max_length=50, default="secondary")
    
    # NEW FIELDS for enhanced certification cards (all optional)
    provider = models.CharField(max_length=100, blank=True, help_text="e.g., Coursera, Udemy")
    date_earned = models.DateField(null=True, blank=True)
    expires = models.DateField(null=True, blank=True)
    
    # NEW: Does Not Expire Option
    does_not_expire = models.BooleanField(default=False, help_text="Check if this certification never expires")
    
    credential_id = models.CharField(max_length=50, blank=True, null=True)
    color_rgb = models.CharField(max_length=20, blank=True, default="108,117,125")
    icon_class = models.CharField(max_length=50, blank=True, default="fas fa-certificate")
    icon_url = models.URLField(blank=True, null=True)
    verification_url = models.URLField(blank=True, null=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def provider_name(self):
        """Fallback to 'cert' field if provider is empty"""
        return self.provider or self.cert or "Independent"
    
    @property
    def formatted_date_earned(self):
        """Format date for template"""
        return self.date_earned.strftime("%b %Y") if self.date_earned else None
    
    @property
    def formatted_expires(self):
        """Show expiry date OR 'Never Expires'"""
        if self.does_not_expire:
            return "Never Expires"
        return self.expires.strftime("%b %Y") if self.expires else None
    
    @property
    def has_expiry(self):
        """Helper for template - true if has expiry date AND not lifetime"""
        return bool(self.expires and not self.does_not_expire)

class Stat(models.Model):
    label = models.CharField(max_length=100, unique=True)
    value = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    color_class = models.CharField(max_length=50, default="primary")

    class Meta:
        ordering = ['label']
    
    def __str__(self):
        return self.label


from django.db import models
from django.utils.text import slugify

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)  # ← ADD null=True
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='projects/', blank=True)
    category = models.CharField(max_length=100, default='Django')
    technologies = models.TextField(blank=True)  # "Django, PostgreSQL, React"
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
from django.db import models
from django.utils.text import slugify

class Badge(models.Model):
    name = models.CharField(max_length=100)
    skill = models.CharField(max_length=100, help_text="Specific skill e.g., 'Django ORM'")
    issuer = models.CharField(max_length=100, help_text="e.g., Coursera, Credly")
    image = models.ImageField(upload_to='badges/', blank=True, null=True)
    verification_url = models.URLField(blank=True, null=True)
    date_earned = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.skill} - {self.issuer}"

    class Meta:
        ordering = ['-created_at']

class Education(models.Model):
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=200)
    duration = models.CharField(max_length=50)
    percentage_or_cgpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)  # e.g., 8.45 or 85.50
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default="fas fa-graduation-cap")

    def __str__(self):
        return f"{self.degree} - {self.institution}"

    class Meta:
        ordering = ['-duration']
        verbose_name_plural = "Educations"