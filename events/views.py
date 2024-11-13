from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
)
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm, EventForm
from .models import Event


# Create your views here.
def home(request):
    return render(request, "events/home.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "events/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "events/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def profile_view(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, "events/profile.html", {"form": form})


@login_required
def my_events(request):
    events = Event.objects.filter(user=request.user)
    return render(request, "events/my_events.html", {"events": events})


@login_required
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            form.save()
            return redirect("home")
    else:
        form = EventForm()
    return render(request, "events/create_event.html", {"form": form})


@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    return render(request, "events/event_detail.html", {"event": event})


@login_required
def event_update(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this event.")

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("my_events")
    else:
        form = EventForm(instance=event)

    return render(request, "events/event_update.html", {"form": form, "event": event})


@login_required
def event_delete(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
        if event.user == request.user:
            event.delete()
            return redirect("my_events")
        else:
            return HttpResponse("You are not allowed to delete this event", status=403)
    except Event.DoesNotExist:
        return HttpResponse(
            """
            <div style="text-align: center;">
                <h1>Event doesn't exist!</h1>
                <h2><a href="/my-events/">Go to My Events</a></h2>
            </div>
        """
        )
