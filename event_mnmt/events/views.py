from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Event, EventRegistration

# -------------------------------
# Event list page
# -------------------------------
@login_required
def event_list(request):
    events = Event.objects.all()
    user_registered_events = EventRegistration.objects.filter(user=request.user)
    registered_event_ids = [reg.event.id for reg in user_registered_events]
    return render(request, "events/event_list.html", {
        "events": events,
        "registered_event_ids": registered_event_ids
    })


# -------------------------------
# Event detail page
# -------------------------------
@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, "events/event_detail.html", {"event": event})


# -------------------------------
# Register for an event
# -------------------------------
@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registration, created = EventRegistration.objects.get_or_create(user=request.user, event=event)

    if created:
        messages.success(request, f"You have successfully registered for {event.title}!")
        return redirect('registration_success')
    else:
        messages.info(request, f"You are already registered for {event.title}.")

    return redirect('event_list')


# -------------------------------
# Registration success page
# -------------------------------
@login_required
def registration_success(request):
    return render(request, "events/registration_success.html")


# -------------------------------
# Dashboard page
# -------------------------------
@login_required
def dashboard(request):
    created = Event.objects.filter(organizer=request.user)
    registered = EventRegistration.objects.filter(user=request.user)
    return render(request, "events/dashboard.html", {
        "created": created,
        "registered": registered
    })


# -------------------------------
# User signup page
# -------------------------------
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("event_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


# -------------------------------
# Profile page
# -------------------------------
@login_required
def profile(request):
    return render(request, "events/profile.html")
