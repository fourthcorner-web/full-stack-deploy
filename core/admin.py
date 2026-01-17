from django.contrib import admin
from django.utils.html import format_html
from .models import Job, Post, PostSection



@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'division', 'location', 'is_active', 'posted_date')
    list_filter = ('division', 'is_active', 'posted_date')
    search_fields = ('title', 'description', 'requirements')
    list_editable = ('is_active',)
    ordering = ('-posted_date',)

class PostSectionInline(admin.StackedInline): 
    model = PostSection
    extra = 0
    # We include 'order' here so the JavaScript can find it and update it
    fields = ('order', 'heading', 'text_content', 'image')
    # Default Django ordering for the inline rows
    ordering = ('order',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('display_thumbnail', 'title', 'created_at')
    list_display_links = ('display_thumbnail', 'title') 
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PostSectionInline]
    # Performance optimization: reduce database queries
    list_select_related = ('author',)
    prefetch_related = ('sections',)

    # This connects the jQuery UI drag-and-drop to your Admin
    class Media:
        js = (
            'https://code.jquery.com/ui/1.12.1/jquery-ui.min.js',
            'js/admin_sortable.js',
        )
        css = {
            'all': ('css/admin_custom.css',)
        }

    def display_thumbnail(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="width: 50px; height: auto; border-radius: 4px; border: 1px solid #f02d2d;" />', obj.thumbnail.url)
        return "No Image"
    display_thumbnail.short_description = 'Thumbnail'






from django.contrib import admin
from django.contrib import messages  # Added for notifications
from .models import Project, ProjectSection, ProjectCategory

class ProjectSectionInline(admin.StackedInline):
    model = ProjectSection
    extra = 0  # No empty boxes by default
    fields = ('order', 'title', 'description', 'image')
    ordering = ('order',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    # 'is_featured' is the checkbox you'll use to pick the 3 main projects
    list_display = ('title', 'category', 'is_featured', 'status', 'location')
    list_display_links = ('title',)
    list_editable = ('is_featured',) 
    list_filter = ('category', 'is_featured')
    inlines = [ProjectSectionInline]
    # Performance optimization: reduce database queries
    list_select_related = ('category',)
    prefetch_related = ('sections',)

    def save_model(self, request, obj, form, change):
        """
        Custom save logic to notify the admin if more than 3 projects are featured.
        """
        if obj.is_featured:
            # Count other featured projects in this category (excluding the current one)
            featured_count = Project.objects.filter(
                category=obj.category, 
                is_featured=True
            ).exclude(pk=obj.pk).count()
            
            if featured_count >= 3:
                # Triggers a yellow warning banner at the top of the page
                self.message_user(
                    request, 
                    f"Warning: You now have {featured_count + 1} featured projects in '{obj.category}'. "
                    "Your homepage is designed for exactly 3 projects per row.", 
                    level=messages.WARNING
                )
        
        super().save_model(request, obj, form, change)

    class Media:
        js = (
            'https://code.jquery.com/ui/1.12.1/jquery-ui.min.js',
            'js/admin_sortable.js',
        )
        css = {
            'all': ('css/admin_custom.css',)
        }

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    # 'order' allows you to rank industries (e.g., 01, 02, 03)
    list_display = ('order', 'name')
    
    # We make 'name' the link so 'order' can be editable without errors
    list_display_links = ('name',) 
    list_editable = ('order',) 
    
    ordering = ('order',)