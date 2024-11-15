from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
)
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm, EventForm
from .models import Event, Booking
from django.db.models import Q


# Create your views here.
def home(request):
    query = request.GET.get("q", "")
    category = request.GET.get("category", "")
    selected_date = request.GET.get("date", "")

    events = Event.objects.all().order_by("-date")

    if query:
        events = events.filter(Q(name__icontains=query) | Q(location__icontains=query))

    if category:
        events = events.filter(category=category)

    if selected_date:
        events = events.filter(date=selected_date)

    booked_events = []
    if request.user.is_authenticated:
        booked_events = Booking.objects.filter(user=request.user).values_list(
            "event_id", flat=True
        )

    categories = [
        {"code": code, "label": label, "is_selected": (code == category)}
        for code, label in Event.CATEGORY_CHOICES
    ]

    context = {
        "events": events,
        "booked_events": booked_events,
        "query": query,
        "selected_category": category,
        "selected_date": selected_date,
        "categories": categories,
    }

    return render(request, "events/home.html", context)


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
    events = Event.objects.filter(user=request.user).order_by("-date")
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


def event_detail(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
        return render(request, "events/event_detail.html", {"event": event})

    except Event.DoesNotExist:
        return HttpResponse(
            """
            <div style="text-align: center;">
                <h1>Event doesn't exist!</h1>
                <h2><a href="/">Go to Home</a></h2>
            </div>
            """
        )


@login_required
def event_update(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)

        if event.user != request.user and not request.user.is_staff:
            return HttpResponseForbidden("You are not allowed to edit this event.")

        if request.method == "POST":
            form = EventForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                return redirect("my_events")
        else:
            form = EventForm(instance=event)

        return render(
            request, "events/event_update.html", {"form": form, "event": event}
        )

    except Event.DoesNotExist:
        return HttpResponse(
            """
            <div style="text-align: center;">
                <h1>Event doesn't exist!</h1>
                <h2><a href="/my-events/">Go to My Events</a></h2>
            </div>
            """
        )


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


@login_required
def book_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)

        if event.is_fully_booked():
            return HttpResponse(
                """
                <div style="text-align: center;">
                    <h1>This event is fully booked!</h1>
                    <h2><a href="/">Return to Homepage</a></h2>
                </div>
                """
            )

        if Booking.objects.filter(user=request.user, event=event).exists():
            return HttpResponse(
                """
                <div style="text-align: center;">
                    <h1>You have already booked this event!</h1>
                    <h2><a href="/">Return to Homepage</a></h2>
                </div>
                """
            )

        Booking.objects.create(user=request.user, event=event)
        return redirect("my_booked_events")

    except Event.DoesNotExist:
        return HttpResponse(
            """
            <div style="text-align: center;">
                <h1>Event doesn't exist!</h1>
                <h2><a href="/">Go to Home</a></h2>
            </div>
            """
        )


@login_required
def my_booked_events(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "events/my_booked_events.html", {"bookings": bookings})
