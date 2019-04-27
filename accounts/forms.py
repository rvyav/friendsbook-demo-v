from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import (
    authenticate,
    login,
    get_user_model

)
from django.contrib.auth.forms import UserChangeForm

# Import ModelForm
from django.forms import ModelForm
from .models import Profile

Profile = get_user_model()


class UserLoginForm(forms.Form):
    ''' 
    Validate Login form username and password.
    '''
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    ''' 
    Validate Registration form fields.
    '''
    email = forms.EmailField(label='Email address')
    first_name = forms.CharField(label='First name', required=False, help_text='Optional')
    last_name = forms.CharField(label='Last name', required=False, help_text='Optional')
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password2'
        ]
  

    def clean(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Passwords must match")
        return super(UserRegisterForm, self).clean(*args, **kwargs)


class EditProfileForm(UserChangeForm):
    '''
    Edit Profile.
    '''
    assword2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
    

    class Meta:
        model = User 
        fields = (
        'username',
        'first_name',
        'last_name',
        # 'password1',
        # 'password2',
        'email',
        )

    def __init__(self, *args, **kwargs):
        '''
        Delete password field in edit profile page.
        '''
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields.pop('password')                             # check whether this is best practice


class ProfileForm(forms.ModelForm):

    image = forms.ImageField()
    bio = forms.CharField(label='Bio')
    location = forms.CharField(label='Location', required=False, help_text='Optional')


    class Meta:
        model = Profile
        fields = ('bio', 'location', 'image')












