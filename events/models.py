from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Event(models.Model):
    CATEGORY_CHOICES = [
        ("conference", "Conference"),
        ("concert", "Concert"),
        ("workshop", "Workshop"),
        ("seminar", "Seminar"),
        ("others", "Others"),
    ]

    name = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="")
    capacity = models.PositiveIntegerField(default=0)

    def is_fully_booked(self):
        """Check if the event has reached its capacity."""
        return self.bookings.count() >= self.capacity

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "user",
            "event",
        )

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"
