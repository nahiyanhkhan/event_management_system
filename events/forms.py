from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Event


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        exclude = ["password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "password" in self.fields:
            del self.fields["password"]


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name", "date", "location", "description"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }
