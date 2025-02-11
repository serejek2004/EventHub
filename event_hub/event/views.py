from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, UpdateView, DeleteView

from .models import Event
from .forms import EventForm

def index(request):
    events = Event.objects.all().order_by('date_time')
    return render(request, 'event/index.html', {'data': events})

class EventDetailView(DetailView):
    model = Event
    template_name = 'event/detail.html'
    context_object_name = 'event'

class EventUpdateView(UpdateView):
    model = Event
    template_name = 'event/update.html'
    form_class = EventForm

class EventDeleteView(DeleteView):
    model = Event
    success_url = '/event/'

    def post(self, request, *args, **kwargs):
        event = self.get_object()

        if event.creator != request.user:
            return HttpResponseRedirect(reverse('event:index'))

        event.delete()
        return HttpResponseRedirect(self.success_url)

@login_required
def event_create(request):
    errors = ''
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            return redirect(f'event_detail', slug=event.slug)
        else:
            errors = form.errors

    form = EventForm()
    return render(request, 'event/create.html', {'form': form, 'errors': errors})
