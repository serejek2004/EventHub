import os
import sys
from django.utils.text import slugify
from event.models import Event


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_hub.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    for event in Event.objects.all():
        if not event.slug:
            event.slug = slugify(event.title)
            event.save()
    main()
