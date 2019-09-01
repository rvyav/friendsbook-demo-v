from django.urls import path, include
from django.contrib import admin
from . import views

from django.views.decorators.cache import cache_page

from .views import (
	PostListView,
	PostCreateView,
	PostUpdateView,
	PostDetailView,
	PostDeleteView
)

# Errors
from django.conf.urls import (
    handler404, 
    handler500
)


handler404 = 'accounts.views.custom_404'
handler500 = 'accounts.views.custom_500'


app_name = 'posts'
urlpatterns = [
	path('feed/', PostListView.as_view(), name='posts-list'),
	path('<int:pk>/', PostDetailView.as_view(), name='posts-details'),
	path('new/', views.PostCreateView.as_view(), name='posts-create'),	
	path('<int:pk>/update/', views.PostUpdateView.as_view(), name='posts-update'),
	# the template below is to confirm deletion
	path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='posts-delete'),	 

]