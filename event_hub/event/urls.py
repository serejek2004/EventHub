from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='event'),
    path('create', views.event_create, name='event_create'),
    path('<slug:slug>', views.EventDetailView.as_view(), name='event_detail'),
    path('<slug:slug>/update', views.EventUpdateView.as_view(), name='event_update'),
    path('<slug:slug>/delete', views.EventDeleteView.as_view(), name='event_delete'),
]