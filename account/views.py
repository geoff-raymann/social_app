from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from bookmarks import settings
from django.contrib.auth.models import User, auth
from .models import Profile
from django.contrib import messages
import requests
import json


# Create your views here.

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            global new_user
            new_user = user_form.save(commit=False)
            
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # Create a new user Profile
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {
                'new_user': new_user
            })
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {
        'user_form':user_form
    })

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {
        'form':form
    })


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {
        'section': dashboard
    })

def logout(request):
    auth.logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {
        'user_form': user_form,
        'profile_form':profile_form
    })


# def authenticate_user(request):
#     if request.method == 'GET':
#         # Get the code from the URL query string
#         code = request.GET.get('code')
#         # Prepare the parameters for the access token request
#         params = {
#             'client_id': '3434741986771292',
#             'redirect_uri': 'https://mysite.com:800/account/login',
#             'client_secret': '9b93253f9de28e74001ef64c31ebfe3c',
#             'code': code
#         }
#         # Send the access token request to Facebook
#         response = requests.get('https://graph.facebook.com/v8.0/oauth/access_token', params=params)
#         # Extract the access token from the response
#         access_token = response.json().get('access_token')
#         # Use the access token to get the user's profile information
#         profile_response = requests.get(f'https://graph.facebook.com/v8.0/me?access_token={access_token}&fields=id,name,email')
#         # Extract the user's profile information
#         profile = profile_response.json()
#         # Store the user's profile information in the session
#         request.session['user_profile'] = profile
#         # Redirect the user to the home page
#         return redirect('account:dashboard')



#         # Define the API endpoint
#         url = "https://graph.facebook.com/v9.0/me?fields=id,name,email&access_token=" + access_token

#         # Make the API request
#         response = requests.get(url)

#         # Check if the request was successful
#         if response.status_code == 200:
#             # Load the JSON data from the response
#             data = json.loads(response.text)
#             print("User ID:", data["id"])
#             print("Name:", data["name"])
#             print("Email:", data["email"])
#         else:
#             print("Failed to retrieve user data from Facebook API")

            
