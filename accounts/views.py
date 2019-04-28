from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


from django.contrib.auth import (
    authenticate,
    get_user_model
)

#from django.contrib.auth.views import login as auth_login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import login, logout
from .forms import (
    UserLoginForm, 
    UserRegisterForm, 
    EditProfileForm,
    ProfileForm
)

from django.contrib.auth import update_session_auth_hash

from .models import Profile, Friend

from posts.models import Post


from django.http import HttpResponseRedirect # For FriendRequest

from django.contrib.auth.models import User    # Added for pk and friend requests

from django.utils.decorators import method_decorator # Decorate class based views

from django.views.decorators.cache import cache_page # cache

# Errors
from django.http import Http404

def index(request):
    pass
    return render(request, "accounts/index.html")



def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)   
        # yellow 'password' means from password data submitted in forms, give me password in 'white'
        login(request, user)
        if next:
            return redirect(next)
        return redirect('posts:posts-list')

    context = {
        'form': form
    }
    return render(request, "accounts/login.html", context)


def register(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('accounts:login')

    context = {
        'form': form
    }
    return render(request, "accounts/register.html", context)


@login_required
@cache_page(60 * 10)
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        extended_profile_form = ProfileForm(request.POST,        # Populate image data if POST
                                            request.FILES,
                                            instance=request.user.profile)
        
        if form.is_valid() and extended_profile_form.is_valid():
            form.save()
            extended_profile_form.save()
            return redirect('accounts:profile')

    else:
        form = EditProfileForm(instance=request.user)
        extended_profile_form = ProfileForm(instance=request.user.profile)


    context = {
            'form':form,
            'extended_profile_form':extended_profile_form
    }

    return render(request, 'accounts/edit-profile.html', context)
    
# After changes below
@login_required
@cache_page(60 * 10)
def current_user_profile(request, pk):
    ''' PK of the user page clicked on.'''
    user=get_object_or_404(User, pk=pk)
    profile = Profile.objects.all()
    posts = Post.objects.filter(author=user.pk)
    context = {'profile':profile, 'user':user, 'me':request.user, 'posts':posts} # added user for pk
    return render(request, 'accounts/profile.html', context) 
     

@login_required
@cache_page(60 * 10)
def profile(request):
    ''' User who authenticated.'''
    profile = Profile.objects.all()
    posts = Post.objects.filter(author=request.user)    # (request) means the user who has authenticated
    context = {'profile':profile, 'user':request.user, 'me':request.user, 'posts':posts}
    return render(request, 'accounts/profile.html', context)  


@login_required
def change_password(request):

    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('accounts:profile')

    else:
        form = PasswordChangeForm(user=request.user)

    context = {'form':form} 
    return render(request, 'accounts/change-password.html', context)

@login_required
@cache_page(60 * 10)
def friends_list(request, *args, **kwargs):
    posts = Post.objects.all()
    users = User.objects.exclude(id=request.user.id).order_by("id")        # five_users = users.order_by("id")[:3]
        
    try:
        friend = Friend.objects.get(current_user=request.user)         # Create a list of friends in relationship with
        friends = friend.friend_user.all()                              # Create a list of friends in relationship with
    except:
        friends = Friend.objects.none()                                 # in case there is no relationship start with zero
    context = {
            'posts':posts,
            'users':users,
            'friends':friends
        }

    return render(request, "accounts/friends-list.html", context) 


@login_required
@cache_page(60 * 10)
def users_list(request, *args, **kwargs):
    posts = Post.objects.all()
    users = User.objects.exclude(id=request.user.id).order_by("id")        # five_users = users.order_by("id")[:3]
        
    try:
        friend = Friend.objects.get(current_user=request.user)             # Create a list of friends in relationship with
        friends = friend.friend_user.all()                                 # Create a list of friends in relationship with
    except:
        friends = Friend.objects.none()                                    # in case there is no relationship start with zero
    context = {
            'posts':posts,
            'users':users,
            'friends':friends
        }

    return render(request, "accounts/users-list.html", context)            


def add_friend(request, pk):
    ''' 
    Add friend in Home Page
    '''
    new_friend = User.objects.get(pk=pk)
    Friend.make_friend(request.user, new_friend)
    return redirect('posts:posts-list')

def add_friend_from_users_list(request, pk):
    ''' 
    Add friend.
    '''
    new_friend = User.objects.get(pk=pk)
    Friend.make_friend(request.user, new_friend)
    return redirect('accounts:users-list')

def remove_friend(request, pk):
    ''' 
    Remove friend.
    '''
    new_friend = User.objects.get(pk=pk)
    Friend.lose_friend(request.user, new_friend)
    return redirect('accounts:friends-list')


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


# Errors

def custom_404(request):
    return render(request, 'templates/404.html')

def custom_500(request):
    return render(request, 'templates/500.html')

    



