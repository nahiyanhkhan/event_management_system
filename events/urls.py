from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("create-event/", views.create_event, name="create_event"),
    path("my-events/", views.my_events, name="my_events"),
    path("event/<int:event_id>/", views.event_detail, name="event_detail"),
    path("event/<int:event_id>/update/", views.event_update, name="event_update"),
    path("event/<int:event_id>/delete/", views.event_delete, name="event_delete"),
    path("event/<int:event_id>/book/", views.book_event, name="book_event"),
    path("my-booked-events/", views.my_booked_events, name="my_booked_events"),
]
