from django.shortcuts import render

def index(request):
    events = [{
            'title': 'Arduino days',
            'date_time': '15.12.2025',
            'location': 'Lviv, zelena, 85',
            'max_participants': 25,
            'participants': 'Anton, Luka, Andriy',
            'creator': 'Nazar',
            'comments': 99,
        },
        {
            'title': 'Arduino days',
            'date_time': '15.12.2025',
            'location': 'Lviv, zelena, 85',
            'max_participants': 25,
            'participants': 'Anton, Luka, Andriy',
            'creator': 'Nazar',
            'comments': 99,
        },
        {
            'title': 'Arduino days',
            'date_time': '15.12.2025',
            'location': 'Lviv, zelena, 85',
            'max_participants': 25,
            'participants': 'Anton, Luka, Andriy',
            'creator': 'Nazar',
            'comments': 99,
        }
    ]

    data = {
        'number_of_events': 2,
        'list_of_events': events,
    }
    return render(request, 'event/index.html', {'data': data})
