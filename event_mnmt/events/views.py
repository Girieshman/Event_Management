from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, Registration

@login_required
def event_list(request):
    events = Event.objects.all()
    user_registered_events = request.user.registered_events.all()
    registered_event_ids = [event.id for event in user_registered_events]
    return render(request, "events/event_list.html", {"events": events, "registered_event_ids": registered_event_ids})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, "events/event_detail.html", {"event": event})

@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    Registration.objects.get_or_create(event=event, attendee=request.user)
    return redirect("dashboard")

@login_required
def dashboard(request):
    created = Event.objects.filter(organizer=request.user)
    registered = Registration.objects.filter(attendee=request.user)
    return render(request, "events/dashboard.html", {"created": created, "registered": registered})


from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log the user in immediately
            return redirect("event_list")  # redirect to homepage
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def profile_view(request):
    return render(request, "profile.html")


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, EventRegistration

@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registration, created = EventRegistration.objects.get_or_create(user=request.user, event=event)
    if created:
        messages.success(request, f"You have successfully registered for {event.title}.")
    else:
        messages.info(request, f"You are already registered for {event.title}.")
    return redirect('event_list')  # or wherever you show events

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def profile(request):
    return render(request, "events/profile.html")

