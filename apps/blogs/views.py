from django.views.generic import ListView, DetailView
from .models import Blog

class BlogListView(ListView):
    model = Blog
    paginate_by = 5
    template_name = "blog/blog_list.html"

class BlogDetailView(DetailView):
    model = Blog
    template_name = "blog/blog_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"