from django.urls import path 
from django.contrib.auth.decorators import login_required
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'


urlpatterns = [
	path('', login_required(views.post_list), name='post_list'),
	#path('', views.PostList.as_view(), name='post_list'),
	path('<int:year>/<int:month>/<int:day>/<slug:post>/',
		 login_required(views.post_detail), name='post_detail'),
	path('<int:post_id>/share/', login_required(views.post_share),
	     name='post_share'),
	path('tag/<slug:tag_slug>/', login_required(views.post_list),
		 name='post_list_by_tag'),
		path('feed/', LatestPostsFeed(), name='post_feed'),
	path('search/', login_required(views.post_search), name='post_search'),
	path('login/', views.login_user, name='login_user'),
	path('logout/', views.logout_user, name='logout_user')
]