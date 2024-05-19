from django.urls import path

from streams.views import (
    get_new_posts,
    start,
    stream_new_activity_and_presence,
    stream_timer,
)

app_name = "streams"

urlpatterns = [
    path("timer/", stream_timer, name="timer"),
    path(
        "listen-with-status/",
        stream_new_activity_and_presence,
        name="streams-listen-with-status",
    ),
    path("new/<str:last_id_returned>/", get_new_posts, name="streams-new"),
    path("", start, name="streams-content"),
]
