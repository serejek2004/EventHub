from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, UpdateView, DeleteView

from profile.models import UserProfile
from .models import Event
from .forms import EventForm

def index(request):
    events = Event.objects.all().order_by('date_time')
    return render(request, 'event/index.html', {'data': events, 'user': request.user})

def event_details(request, slug):
    event = get_object_or_404(Event, slug=slug)

    if request.user.is_authenticated:
        user = get_object_or_404(UserProfile, user__id=request.user.id)

        if user in event.participants.all():
            data = {"event": event, 'registered': True}
        else:
            data = {"event": event, 'registered': False}

        return render(request, 'event/detail.html', data)

    return render(request, 'event/detail.html', {"event": event})

def event_update(request, slug):
    event = get_object_or_404(Event, slug=slug)

    if request.user != event.creator:
        return HttpResponseForbidden("You are not allowed to edit this event.")

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect(reverse('event_detail', kwargs={'slug': event.slug}))
    else:
        form = EventForm(instance=event)

    return render(request, 'event/update.html', {'form': form, 'event': event, 'errors': form.errors})

def event_delete(request, slug):
    event = get_object_or_404(Event, slug=slug)

    if request.user != event.creator:
        return HttpResponseForbidden("You are not allowed to edit this event.")

    event.delete()
    return redirect('event')

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            creator_profile = get_object_or_404(UserProfile, user=request.user)
            event.participants.add(creator_profile)
            return redirect(f'event_detail', slug=event.slug)
        else:
            data = {'form': form, 'errors': form.errors}
            return render(request, 'event/create.html', data)

    form = EventForm()
    data = {'form': form, 'errors': form.errors}
    return render(request, 'event/create.html', data)

def not_auth_event_create(request):
    return render(request, 'event/create.html')


def registration_to_event(request, slug, username):
    print("reg")
    event = get_object_or_404(Event, slug=slug)
    user = get_object_or_404(UserProfile, user__username=username)

    if event.participants.count() < event.max_participants:

        if user not in event.participants.all():
            event.participants.add(user)
            event.save()
        else:
            data = {"event": event, 'registered': True}
            return render(request, 'event/detail.html', data)

        return redirect('event_detail', slug=slug)

    else:
        data = {"event": event, 'errors': 'the maximum number of people registered'}
        return render(request, 'event/detail.html', data)


def unregister_to_event(request, slug, username):
    event = get_object_or_404(Event, slug=slug)
    user = get_object_or_404(UserProfile, user__username=username)
    print("lol")
    if user in event.participants.all():
        print("hello")
        event.participants.remove(user)
        event.save()

    return redirect('event_detail', slug=slug)
