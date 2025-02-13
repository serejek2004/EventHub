from django.shortcuts import render, get_object_or_404

from profile.models import UserProfile


def index(request):
    data = {}
    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        data = {'slug': user_profile.slug}
    return render(request, 'main/index.html', data)
