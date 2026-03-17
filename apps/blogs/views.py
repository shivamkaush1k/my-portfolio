from django.views.generic import ListView, DetailView
from .models import Blog

class BlogListView(ListView):
    model = Blog
    paginate_by = 5
    template_name = "blogs/blog_list.html"

class BlogDetailView(DetailView):
    model = Blog
    template_name = "blogs/blog_detail.html"
    slug_field = "slug"      # Match model field
    slug_url_kwarg = "slug"  # Match URL pattern
    context_object_name = 'object'
