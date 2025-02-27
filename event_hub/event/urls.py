from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='event'),
    path('create', views.event_create, name='event_create'),
    path('<slug:slug>', views.event_details, name='event_detail'),
    path('<slug:slug>/update', views.event_update, name='event_update'),
    path('<slug:slug>/delete', views.event_delete, name='event_delete'),
    path('<slug:slug>/<str:username>/register', views.registration_to_event, name='registration_to_event'),
    path('<slug:slug>/<str:username>/unregister', views.unregister_to_event, name='unregister_to_event'),
    path('<slug:slug>/commenting', views.commenting, name='commenting'),
    path('<slug:slug>/delete-comment/<int:comment_id>', views.comment_delete, name='delete-comment'),
    path('like-comment/<int:comment_id>', views.comment_like, name='like-comment'),
    path('dislike-comment/<int:comment_id>', views.comment_dislike, name='dislike-comment'),
    path('delete-reaction/<int:comment_id>', views.delete_reaction, name='delete_reaction'),
]