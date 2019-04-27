from django.contrib import admin
from django.urls import path, include
from . import views

# Errors
from django.conf.urls import (
    handler404, handler500 #Errors
)


handler404 = 'accounts.views.custom_404'
handler500 = 'accounts.views.custom_500'


app_name = 'accounts'
app_name = 'accounts'
urlpatterns = [
	path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:pk>/', views.current_user_profile, name='profile-with-pk'),
    path('add-friend/<int:pk>/', views.add_friend, name='add-friend'),  # changed to two urls below: form profile and user_list
    path('add-friend-from-users-list/<int:pk>/', views.add_friend_from_users_list, name='add-friend-from-users-list'),
    path('remove-friend/<int:pk>/', views.remove_friend, name='remove-friend'),
    #path('connect/<int:pk>/', views.change_friends, name='change-friends'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('friends-list/', views.friends_list, name='friends-list'),
    path('users-list/', views.users_list, name='users-list'),
    #path('invitation-manager/', views.invitation_manager, name='invitation-manager'),
	path('change-password/', views.change_password, name='change-password'),
    path('logout/', views.logout_view, name='logout')
]