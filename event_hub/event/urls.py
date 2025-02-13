from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='event'),
    path('create/auth-error', views.not_auth_event_create, name='not_auth_event_create'),
    path('create', views.event_create, name='event_create'),
    path('<slug:slug>', views.event_details, name='event_detail'),
    path('<slug:slug>/update', views.event_update, name='event_update'),
    path('<slug:slug>/delete', views.event_delete, name='event_delete'),
    path('<slug:slug>/<str:username>/register', views.registration_to_event, name='registration_to_event'),
    path('<slug:slug>/<str:username>/unregister', views.unregister_to_event, name='unregister_to_event'),
]