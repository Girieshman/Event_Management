from django.urls import path
from . import views

urlpatterns = [
    path("", views.event_list, name="event_list"),
    path('register/<int:event_id>/', views.register_event, name='register_event'),
    path("<int:event_id>/register/", views.register_event, name="register_event"),
    path('success/', views.registration_success, name='registration_success'),
    path("event/<int:event_id>/", views.event_detail, name="event_detail"),
    path("profile/", views.profile, name="profile"),
    path("event/<int:event_id>/register/", views.register_event, name="register_event"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
