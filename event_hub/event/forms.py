from django.core.exceptions import ValidationError

from .models import Event
from django.forms import ModelForm, TextInput, Textarea, FileInput, NumberInput, DateTimeInput


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'date_time', 'max_participants', 'event_image']

        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Event Title',
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Event Description',
            }),
            'location': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Event Location',
            }),
            'date_time': DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Event Date',
            }),
            'max_participants': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Event Max Participants',
            }),
            'event_image': FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Event Image',
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Event.objects.filter(title=title).exclude(id=self.instance.id).exists():
            raise ValidationError(f"The title '{title}' is already taken.")
        return title