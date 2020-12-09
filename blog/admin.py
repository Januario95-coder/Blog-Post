from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ['title', 'slug', 'author', 'profile_image',
					'publish', 'status']
	list_filter = ['title', 'author', 'status']
	prepopulated_fields = {'slug': ('title',)}
	search_fields = ['title', 'body']
	#raw_id_fields = ['author']
	date_hierarchy = 'publish'
	ordering = ['status', '-publish']
	list_editable = ['status', 'profile_image']
	list_per_page = 5
	
	

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ['name', 'email', 'post', 
					'created', 'active']
	list_filter = ['active', 'created', 'updated']
	search_fields = ['name', 'email', 'body']
	ordering = ['created']
	list_editable = ['active']
	list_per_page = 5