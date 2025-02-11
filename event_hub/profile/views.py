from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect


from .models import Profile
from .forms import RegistrationForm, LoginForm


# Create your views here.
def profile(request):
    return render(request, 'profile/profile.html')


def login(request):
    errors = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
        else:
            errors = "Incorrect username or password"

    form = LoginForm()
    return render(request, 'profile/login.html', {'form': form, 'errors': errors})

def register(request):
    errors = ''
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user = form.save(commit=False)
            user.save()
            user_profile = Profile(user=user)
            user_profile.save()
            return redirect('home')
        else:
            errors = form.errors

    form = RegistrationForm()
    return render(request, 'profile/registration.html', {'form': form, 'errors': errors})

def logout(request):
    return render(request, 'main/index.html')

