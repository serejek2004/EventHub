from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls.base import reverse
from .forms import UserRegistrationForm, UserLoginForm, UserProfileInfoUpdateForm, PasswordUpdateForm
from .models import UserProfile


def not_auth_profile(request):
    return render(request, 'profile/profile.html')


def profile(request, slug):
    user_profile = get_object_or_404(UserProfile, slug=slug)
    is_owner = user_profile.user == request.user
    data = {"profile": user_profile, 'is_owner': is_owner}
    return render(request, 'profile/profile.html', data)


@login_required
def profile_update(request, slug):
    user_profile = get_object_or_404(UserProfile, slug=slug)
    is_owner = user_profile.user == request.user

    if is_owner:
        if request.method == 'POST':
            form = UserProfileInfoUpdateForm(request.POST, request.FILES)
            form.user = request.user

            if form.is_valid():
                form.save(request.user)
                return redirect(reverse('profile', kwargs={'slug': user_profile.slug}))

            else:
                data = {'form': form, 'profile': user_profile}
                return render(request, 'profile/update.html', data)

        else:
            form = UserProfileInfoUpdateForm(initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'age': user_profile.age,
                'biography': user_profile.biography,
                'profile_picture': user_profile.profile_picture,
            })
            data = {'form': form, 'profile': user_profile}
            return render(request, 'profile/update.html', data)

    else:
        return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user).save()
            return redirect('home')
        else:
            data = {'form': form}
            return render(request, 'profile/registration.html', data)
    else:
        form = UserRegistrationForm()

    data = {'form': form}
    return render(request, 'profile/registration.html', data)


def login_user(request):
    errors = False
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username.lower(), password=password)
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                errors = True
    else:
        form = UserLoginForm()

    data = {'form': form, 'errors': errors}
    return render(request, 'profile/login.html', data)


@login_required
def logout_user(request):
    logout(request)
    return redirect('home')


def password_update(request, slug):
    if request.method == 'POST':
        form = PasswordUpdateForm(user=request.user, data=request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            request.user.set_password(new_password)
            request.user.save()
            return redirect('home')
    else:
        form = PasswordUpdateForm(user=request.user)
        return render(request, 'profile/change_password.html', {'form': form})
