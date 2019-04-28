from django.urls import path, include
from django.contrib import admin
from . import views
# Cache
from django.views.decorators.cache import cache_page
# Import CBV
from .views import (
	PostListView,
	PostCreateView,
	PostUpdateView,
	PostDetailView,
	PostDeleteView
)

# Errors
from django.conf.urls import (
    handler404, handler500 #Errors
)


handler404 = 'accounts.views.custom_404'
handler500 = 'accounts.views.custom_500'

# Post create share the same template as Post update View
# Use 'Post_form' for Post Create and Post Update View


app_name = 'posts'
urlpatterns = [
	path('feed/', PostListView.as_view(), name='posts-list'), # URL fetch from Posts, does not need additional URL from URL Post, need view though
	path('<int:pk>/', PostDetailView.as_view(), name='posts-details'),
	path('new/', views.PostCreateView.as_view(), name='posts-create'),	
	path('<int:pk>/update/', views.PostUpdateView.as_view(), name='posts-update'),
	path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='posts-delete'),	# the template is to confirm deletion

]