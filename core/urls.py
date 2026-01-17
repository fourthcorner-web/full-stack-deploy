from django.urls import path
from . import views

urlpatterns = [
    # --- Public Pages ---
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.service, name='service'),
    path('contact/', views.contact, name='contact'),
    path('career/', views.career, name='career'),
    
    # --- Professional Blog Pages ---
    path('blog/', views.blog_list, name='blog_list'), 
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    
    # --- Industrial Service Pages ---
    path('fire-industry/', views.fire_industry, name='fire_industry'),
    path('electrical-systems/', views.electrical_systems, name='electrical_systems'),
    path('construction/', views.construction, name='construction'),


    path('projects/', views.project_list_view, name='project'),
    path('industry/<int:category_id>/', views.industry_all_projects, name='industry_detail'),

]