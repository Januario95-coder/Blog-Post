from django.shortcuts import (
	render, get_object_or_404, redirect
)
from django.views.generic import ListView
from django.core.paginator import (
	Paginator, EmptyPage, PageNotAnInteger
)
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import (
	SearchVector, SearchQuery, SearchRank
)
from django.contrib.auth.decorators import (
	login_required
)
from django.contrib.auth import (
	authenticate, login, logout
)
from .models import Post, Comment
from .forms import (
	EmailPostForm, CommentForm,
	SearchForm, UserLogin
)
import os


class PostList(ListView):
	queryset = Post.published.all()
	context_object_name = 'posts'
	paginate_by = 3
	template_name = 'blog/post/list.html'



# @login_required
def post_list(request, tag_slug=None):
	object_list = Post.published.all()
	tag = None

	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		object_list = object_list.filter(tags__in=[tag])



	paginator = Paginator(object_list, 4)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)



	search_form = SearchForm()
	query = None
	results = []
	if 'query' in request.GET:
		search_form = SearchForm(request.GET)
		if search_form.is_valid():
			query = search_form.cleaned_data['query']
			search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
			search_query = SearchQuery(query)
			results = Post.objects.annotate(
				rank=SearchRank(search_vector, search_query)
			).filter(rank__gte=0.3).order_by('-rank')

	return render(request,
				  'blog/post/list.html',
				  {'posts': posts,
				   'page': page,
				   'tag': tag,
				   'search_form': search_form,
                   'query': query,
                   'results': results})


# @login_required
def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post,
							 slug=post,
							 status='published',
							 publish__year=year,
							 publish__month=month,
							 publish__day=day)


	comments = post.user_comments.filter(active=True)
	#print(post.user_comments)
	new_comment = None
	comment_form = None

	if request.method == 'POST':
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.post = post
			new_comment.save()

		comment_form = CommentForm()
	else:
		comment_form = CommentForm()


	search_form = SearchForm()
	query = None
	results = []
	if 'query' in request.GET:
		search_form = SearchForm(request.GET)
		if search_form.is_valid():
			query = search_form.cleaned_data['query']
			search_vector = SearchVector('title', 'body')
			search_query = SearchQuery(query)
			results = Post.objects.annotate(
                search=search_vector,
                rank=SearchVector(search_vector, search_query),
            ).filter(search=search_query).order_by('-rank')


	post_tags_ids = post.tags.values_list('id', flat=True)
	similar_posts = Post.published.filter(tags__in=post_tags_ids)\
								  .exclude(id=post.id)
	similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
								 .order_by('-same_tags', '-publish')[:4]

	return render(request,
				  'blog/post/detail.html',
				  {'post': post,
				   'comments': comments,
				   'new_comment': new_comment,
				   'comment_form': comment_form,
				   'similar_posts': similar_posts,
				   'search_form': search_form,
                   'query': query,
                   'results': results})

# @login_required
def post_share(request, post_id):
	post = get_object_or_404(Post,
				id=post_id, status='published')
	sent = False


	if request.method == 'POST':
		form = EmailPostForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = f'{cd["name"]} ({cd["email"]}) recommends you reading "{post.title}"'
			message = f'Read "{post.title}" at {post_url}\n\n{cd["name"]}\'s commentds at {cd["comments"]}'
			send_mail(subject, message,
					  os.environ.get('USER_EMAIL2'),
					  [cd['to']])
			sent = True

	else:
		form = EmailPostForm()

	return render(request,
				'blog/post/share.html',
				{'post': post,
				 'form': form,
				 'sent': sent})


# @login_required
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            results = Post.objects.annotate(
                search=search_vector,
                rank=SearchVector(search_vector, search_query),
            ).filter(search=search_query).order_by('-rank')
    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})



def login_user(request):
	form = UserLogin()
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username,
							password=password)

		if user is not None:
			login(request, user)
			print(f'{user} was logged in successfully!')
			return redirect('/blog/')
		else:
			print('Wrong credentials')
			return redirect('/blog/login')

	else:
		form = UserLogin()

	return render(request,
				  'blog/auth/login.html',
				  {'form': form})


def logout_user(request):
	logout(request)
	return redirect('/blog/login/')


def profile(request):
	user = request.user
	post = Post.objects.filter(author=user)
	image = post.first().profile_image
	search_form = SearchForm()
	return render(request,
				  'blog/auth/profile.html',
				  {'user': user,
				   'image': image,
				   'search_form': search_form})
