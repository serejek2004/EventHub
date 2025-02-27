from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Event, EventComment
from django.forms import ModelForm, TextInput, Textarea, FileInput, NumberInput, DateTimeInput


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'date_time', 'max_participants', 'event_image']

        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Event Title',
                'required': 'required',
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Event Description',
                'required': 'required',
            }),
            'location': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Event Location',
                'required': 'required',
            }),
            'date_time': DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Event Date',
                'type': 'datetime-local',
                'required': 'required',
            }),
            'max_participants': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Event Max Participants',
                'required': 'required',
            }),
            'event_image': FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Event Image',
                'required': 'required',
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Event.objects.filter(title=title).exclude(id=self.instance.id).exists():
            raise ValidationError(f"The title '{title}' is already taken.")
        if len(title) < 2:
            raise ValidationError("Title must be longer than 1 symbol.")
        return title

    def clean_date_time(self):
        date_time = self.cleaned_data.get('date_time')
        if date_time:
            if timezone.is_naive(date_time):
                date_time = timezone.make_aware(date_time, timezone.get_current_timezone())

            if date_time < timezone.now():
                raise ValidationError("Date cannot be in the past.")
        return date_time

    def clean_max_participants(self):
        max_participants = self.cleaned_data.get('max_participants')
        if max_participants < 2:
            raise ValidationError("Min participants is 2.")
        return max_participants


class EventCommentForm(ModelForm):
    class Meta:
        model = EventComment
        fields = ['text']
        widgets = {
            'text': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Comment text...',
            })
        }
