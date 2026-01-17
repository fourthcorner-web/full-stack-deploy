
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from .models import ProjectCategory, Project, Job, Post



def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def service(request):
    return render(request, 'service.html')


def contact(request):
    return render(request, 'contact.html')

def fire_industry(request):
    return render(request, 'fire-industry.html')

def electrical_systems(request):
    return render(request, 'electrical-systems.html')

def construction(request):
    return render(request, 'construction.html')

def career(request):
    jobs = Job.objects.filter(is_active=True)
    html_content = render_to_string('career.html', {'jobs': jobs}, request=request)
    return HttpResponse(html_content)

# --- PROFESSIONAL BLOG FRONTEND ---

def blog_list(request):
    # Fetch posts with pre-ordered sections and author to avoid N+1 queries
    posts_list = Post.objects.select_related('author').all().order_by('-created_at')
    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    recent_posts = Post.objects.select_related('author').all().order_by('-created_at')[:5]
    return render(request, 'blog.html', 
                    {
                        'page_obj': page_obj,
                        'recent_posts': recent_posts
                        })

def blog_detail(request, slug):
    # Fetch post with sections and author to avoid N+1 queries
    post = get_object_or_404(Post.objects.select_related('author').prefetch_related('sections'), slug=slug)
    recent_posts = Post.objects.select_related('author').exclude(id=post.id).order_by('-created_at')[:5]
    
    context = {
        'post': post,
        'recent_posts': recent_posts
    }
    return render(request, 'blog-details.html', context)





def project_list_view(request):
    """
    Landing Page: Shows categories with up to 3 manually selected 'Featured' projects.
    """
    # Optimized query: Use Prefetch to filter featured projects at database level
    featured_projects = Prefetch(
        'projects',
        queryset=Project.objects.filter(is_featured=True).order_by('order'),
        to_attr='featured_projects'
    )
    categories = ProjectCategory.objects.prefetch_related(
        featured_projects,
        'projects__sections'
    ).all()
    
    # Slice to 3 projects per category (filtering already done at DB level)
    for category in categories:
        category.featured_projects = category.featured_projects[:3]
        
    return render(request, 'project.html', {'categories': categories})

def industry_all_projects(request, category_id):
    """
    Industry Detail Page: Shows ALL projects for a specific category.
    """
    category = get_object_or_404(ProjectCategory, id=category_id)
    
    # We show the full portfolio here, ordered correctly.
    projects = category.projects.all().order_by('order')
    
    return render(request, 'industry_projects.html', {
        'category': category,
        'projects': projects
    })


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)

def custom_500(request):
    # Handle internal server errors (500) with proper status code
    return render(request, '404.html', status=500)