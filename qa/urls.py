from django.urls import path

from qa.views import (
    create_question,
    get_new_questions,
    questions,
    start,
    stream_new_activity,
    stream_new_activity_and_presence,
    stream_timer,
)

app_name = "realtime"

urlpatterns = [
    path("timer/", stream_timer, name="timer"),
    path("listen/", stream_new_activity, name="qa-listen"),
    path(
        "listen-with-status/",
        stream_new_activity_and_presence,
        name="qa-listen-with-status",
    ),
    path("send/", create_question, name="qa-send"),
    path("<str:name>/", questions, name="qa-questions"),
    path("new/<str:last_id_returned>/", get_new_questions, name="qa-new"),
    path("", start, name="qa"),
]
