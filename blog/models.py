from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from django.urls import reverse
from taggit.managers import TaggableManager

def format_file(file):
	f = file.split('_')
	f = f[0] + f[1] + '.' + f[2].split('.')[-1]

def upload_image_to(instance, filename):
	print(filename)
	#filename = format_file(filename)
	return f"{instance.author}/{filename}"

class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager,
					 self).get_queryset()\
						  .filter(status='published')

class Post(models.Model):
	STATUS_CHOICE = (
		('draft', 'Draft'),
		('published', 'Published')
	)
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250,
				unique_for_date='publish')
	author = models.ForeignKey(User,
						on_delete=models.CASCADE,
						related_name='blog_posts')
	profile_image = models.ImageField(upload_to='images/',
									  default='default.png')
	body = models.TextField()
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10,
							  choices=STATUS_CHOICE,
							  default='draft')
							  
	objects = models.Manager()
	published = PublishedManager()
	
							  
	class Meta:
		ordering = ['-publish',]
		verbose_name = 'Posts'
		verbose_name_plural = 'Posts List'
		
	def __str__(self):
		return self.title
		
		
	
	def get_absolute_url(self):
		return reverse('blog:post_detail',
						args=[self.publish.year,
							  self.publish.month,
							  self.publish.day,
							  self.slug])
							  
	
	tags = TaggableManager()
	
	
	
class Comment(models.Model):
	post = models.ForeignKey(Post,
						on_delete=models.CASCADE,
						related_name='user_comments')
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)
	
	
	class Meta:
		ordering = ['created']
		verbose_name = 'Comments'
		verbose_name_plural = 'Comments List'
		
	def __str__(self):
		return f'Comment by {self.name} on {self.post}'
	
	
	
