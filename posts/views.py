from django.shortcuts import (
	render, 
	redirect, 
	get_object_or_404,
)

from django.views.generic import (
	View,
	ListView,
	FormView,
	CreateView,
	UpdateView,
	DetailView,
	DeleteView,
)
from .models import Post, Comment

from .forms import CommentForm


from django.views.generic.edit import FormMixin		

from accounts.models import Profile, Friend

from django.contrib.auth.decorators import login_required


from django.urls import reverse_lazy	


from django.contrib.auth.mixins import (
	LoginRequiredMixin,
	UserPassesTestMixin	
)


from django.contrib.auth.models import User    


from django.utils.decorators import method_decorator 


from django.views.decorators.cache import cache_page 


class PostListView(LoginRequiredMixin, ListView):
	"""
	Cached dispatch for 10 minutes
	60 * 10 = 10 minutes.
	"""
	model = Post
	context_object_name = 'posts'
	template_name = 'posts/posts-list.html'


	def get(self, request, *args, **kwargs):
		posts = Post.objects.all()
		users = User.objects.exclude(id=self.request.user.id).order_by("id")		
		
		try:
			friend = Friend.objects.get(current_user=self.request.user)						# Create a list of friends in relationship with
			friends = friend.friend_user.all()												# Create a list of friends in relationship with
		except:
			friends = Friend.objects.none()													# in case there is no relationship start with zero
		context = {
				'posts':posts,
				'users':users,
				'friends':friends
		}
		return render(request, self.template_name, context=context)

@method_decorator(cache_page(60 * 10), name='dispatch')
class PostDetailView(LoginRequiredMixin, DetailView):
	model = Post
	template_name = 'posts/posts-details.html'


class PostComment(FormView):
	"""Create a Form for PostDetail."""
	form_class = CommentForm
	template_name = 'posts/posts-details.html'

	def form_valid(self, form):
		form.instance.username = self.request.user
		post = Post.objects.get(pk=self.kwargs['pk'])										
		form.instance.post = post
		form.save()
		return super(PostComment, self).form_valid(form)

	def get_successful_url():
		return reverse('posts:posts-details', kwargs={'pk': self.pk})

class PostDetail(View):
	def get(self, request, *args, **kwargs):
		view = PostComment.as_view()
		return view(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		form.instance.username = self.request.user
		post = Post.objects.get(pk=self.kwargs['pk'])								
		form.instance.post = post
		form.save()
		return super(PostDetail, self).form_valid(form)



class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'description']
	template_name = 'posts/posts-create.html'
	success_url = '/posts/feed'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


@method_decorator(cache_page(60 * 10), name='dispatch')
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'description']
	template_name = 'posts/posts-create.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	template_name = 'posts/posts-confirm-delete.html'
	success_url = '/posts/feed'	# Redirect URL

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False





























