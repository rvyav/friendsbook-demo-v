from django.db import models
from django.urls import reverse		# Redirect from get absolute url
#from accounts.models import User
from django.contrib.auth.models import User
from django.db.models.signals import pre_save 	# Signal for Slug
from django.utils.text import slugify	# import Slugify


class Post(models.Model):
	title = models.CharField(max_length=50)
	slug = models.SlugField(unique=True)		# Required field
	description = models.TextField(max_length=300)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')	#returned the exact name
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		'''
		Redirect to pk detail after creation of PostCreateView. Also connected to pk update.
		'''
		return reverse('posts:posts-details', kwargs={'pk': self.pk })

	class Meta:
		ordering = ['-created_at']

def create_slug(instance, new_slug=None):
	'''
	Recursive function to check 
	whether a Slug exist or not.
	'''
	slug = slugify(instance.title)	# Turn title into Slug
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "{}-{}".format(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
	'''
	Turn title into slug.
	'''
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_username')
	body = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)								# Created to manually deactivate inappropriate comments
