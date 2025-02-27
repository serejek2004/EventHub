from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from profile.models import UserProfile
from .models import Event, EventComment, LikeDislikeComment
from .forms import EventCommentForm, EventForm


def index(request):
    events = Event.objects.all().order_by('date_time')
    return render(request, 'event/index.html', {'data': events, 'user': request.user})


def event_details(request, slug):
    event = get_object_or_404(Event, slug=slug)

    comment_with_info = get_comments_and_reactions(request, event)

    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user__id=request.user.id)

        if user_profile in event.participants.all():
            data = {"event": event, 'registered': True, 'comments_with_info': comment_with_info}
        else:
            data = {"event": event, 'registered': False, 'comments_with_info': comment_with_info}

        return render(request, 'event/detail.html', data)

    data = {"event": event, 'comments_with_info': comment_with_info}
    print(data)
    return render(request, 'event/detail.html', data)


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

def commenting(request, slug):
    event = get_object_or_404(Event, slug=slug)

    if request.method == "POST":
        if request.user.is_authenticated:
            form = EventCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.event = event
                comment.author = get_object_or_404(UserProfile, user__id=request.user.id)
                comment.save()
                return redirect('event_detail', slug=slug)
        else:
            return redirect('login')

    else:
        form = EventCommentForm()

    data = {
        "event": event,
        "comments_with_info": get_comments_and_reactions(request, event),
        "form": form,
        "registered": request.user.is_authenticated
    }
    return render(request, 'event/detail.html', data)

def comment_delete(request, slug, comment_id):
    comment = get_object_or_404(EventComment, id=comment_id)

    if request.user != comment.author.user:
        return HttpResponseForbidden("You are not allowed to edit this comment.")
    else:
        if comment:
            comment.delete()

    return redirect(reverse('event_detail', kwargs={'slug': slug}) + '#event-details-comments')

@login_required()
def comment_like(request, comment_id):
    comment = get_object_or_404(EventComment, id=comment_id)
    LikeDislikeComment.objects.update_or_create(
        user=request.user,
        comment=comment,
        defaults={'value': 1}
    )
    return redirect(reverse('event_detail', kwargs={'slug':comment.event.slug}) + '#event-details-comments')

@login_required()
def comment_dislike(request, comment_id):
    comment = get_object_or_404(EventComment, id=comment_id)
    LikeDislikeComment.objects.update_or_create(
        user=request.user,
        comment=comment,
        defaults={'value': -1}
    )
    return redirect(reverse('event_detail', kwargs={'slug':comment.event.slug}) + '#event-details-comments')

@login_required()
def delete_reaction(request, comment_id):
    LikeDislikeComment.objects.filter(user=request.user, comment_id=comment_id).delete()
    comment = get_object_or_404(EventComment, id=comment_id)
    return redirect(reverse('event_detail', kwargs={'slug':comment.event.slug}) + '#event-details-comments')

def get_likes_count(comment):
    return comment.likes_dislikes.filter(value=1).count()

def get_dislikes_count(comment):
    return comment.likes_dislikes.filter(value=-1).count()

def get_comments_and_reactions(request, event):
    comments = event.comments.all().order_by('-created_at')
    comment_with_info = []
    for comment in comments:
        info_about_comment = {
            "likes": get_likes_count(comment),
            "dislikes": get_dislikes_count(comment),
        }

        if request.user.is_authenticated:
            info_about_comment = {
                "likes": get_likes_count(comment),
                "dislikes": get_dislikes_count(comment),
                "liked_by_user": comment.likes_dislikes.filter(user=request.user, value=1).exists() if True else False,
                "disliked_by_user": comment.likes_dislikes.filter(user=request.user,
                                                                  value=-1).exists() if True else False,
            }

        comment_with_info.append({"comment": comment, "info": info_about_comment})

    return comment_with_info
