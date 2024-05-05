from django.urls import path

from qa.views import (
    create_question,
    get_new_questions,
    questions,
    start,
    stream_new_activity,
)

app_name = "realtime"

urlpatterns = [
    path("qa/listen/", stream_new_activity, name="qa-listen"),
    path("qa/send/", create_question, name="qa-send"),
    path("qa/<str:name>/", questions, name="qa-questions"),
    path("qa/new/<str:last_id_returned>/", get_new_questions, name="qa-new"),
    path("", start, name="qa"),
]
