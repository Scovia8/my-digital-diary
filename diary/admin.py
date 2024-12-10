from django.contrib import admin
from .models import Post
from .models import Comment,BlogPost


admin.site.register(Post)


admin.site.register(Comment)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'content')


# Register your models here.
