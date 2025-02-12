from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls.base import reverse
from .forms import UserRegistrationForm, UserLoginForm, UserProfileInfoUpdateForm
from .models import UserProfile


def not_auth_profile(request):
    return render(request, 'profile/profile.html')


def profile(request, slug):
    profile = get_object_or_404(UserProfile, slug=slug)
    is_owner = profile.user == request.user
    return render(request, 'profile/profile.html', {"profile": profile, 'is_owner': is_owner})


def profile_update(request, slug):
    user_profile = get_object_or_404(UserProfile, slug=slug)
    is_owner = user_profile.user == request.user

    if is_owner:
        if request.method == 'POST':
            form = UserProfileInfoUpdateForm(request.POST, request.FILES)
            if form.is_valid():
                user_profile.user.first_name = form.cleaned_data['first_name']
                user_profile.user.last_name = form.cleaned_data['last_name']
                user_profile.user.email = form.cleaned_data['email']
                user_profile.age = form.cleaned_data['age']
                user_profile.biography = form.cleaned_data['biography']

                if form.cleaned_data['profile_picture']:
                    user_profile.profile_picture = form.cleaned_data['profile_picture']

                user_profile.user.save()
                user_profile.save()

                return redirect(reverse('profile', kwargs={'slug': user_profile.slug}))
            else:

                return render(request, 'profile/update.html', {'form': form, 'profile': user_profile, 'errors': form.errors})
        else:
            form = UserProfileInfoUpdateForm(initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'age': user_profile.age,
                'biography': user_profile.biography,
                'profile_picture': user_profile.profile_picture,
            })
            return render(request, 'profile/update.html', {'form': form, 'profile': user_profile})

    else:
        return redirect('home')


def login_user(request):
    errors = False
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                errors = True
    else:
        print("from")
        form = UserLoginForm()
    return render(request, 'profile/login.html', {'form': form, 'errors': errors})

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user).save()
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm()

    return render(request, 'profile/registration.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('home')
