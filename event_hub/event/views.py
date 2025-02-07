from django.shortcuts import render
from .models import Event

def index(request):

    events = Event.objects.all().order_by('date_time')

    return render(request, 'event/index.html', {'data': events})

def event_detail(request, event_id):
    return render(request, 'event/event_detail.html', {'event_id': event_id})
