import asyncio
import json
import logging
import uuid
from logging import getLogger
from typing import AsyncGenerator

from django.http import HttpRequest, HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from streams.blocker import view_basicauth
from streams.external import ONLINE_STREAM, DataToSend, OnlineStatus, PostService

logger = getLogger(__name__)


@require_http_methods(["GET"])
async def stream_timer(request: HttpRequest, *args, **kwargs):
    async def streamed_events() -> AsyncGenerator[str, None]:
        """Listen for events and generate an SSE message for each event"""
        connection_id = uuid.uuid4()
        events_count = 0

        try:
            logging.info(f"{connection_id}: Connecting to stream")
            while True:
                events_count += 1
                event = "event: new\n"
                event += f"data: {events_count}\n\n"
                logging.info(f"{connection_id}: Sent events. {events_count}")
                yield event
                await asyncio.sleep(1)

        except asyncio.CancelledError:
            logging.info(f"{connection_id}: Disconnected after events. {events_count}")
            raise

    return StreamingHttpResponse(streamed_events(), content_type="text/event-stream")



@view_basicauth
@require_http_methods(["GET"])
async def start(request: HttpRequest) -> HttpResponse:
    stream_server = reverse("streams:streams-listen-with-status")
    messages = []
    return render(
        request,
        "streams/start.html",
        context={"stream_server": stream_server, "messages": messages},
    )


@require_http_methods(["GET"])
async def stream_new_activity_and_presence(request: HttpRequest, *args, **kwargs):

    async def streamed_events() -> AsyncGenerator[str, None]:
        """Listen for events and generate an SSE message for each event"""
        connection_id = str(uuid.uuid4())
        events_count = 0
        listener = PostService()
        last_id_returned = None
        await listener.send_status_to_stream(
            message=OnlineStatus(user=connection_id, status="online")
        )

        try:
            while True:
                message = await listener.listen_on_multiple_streams(
                    last_id_returned=last_id_returned,
                )
                if message:
                    last_id_returned = message[0][1][0][0]
                    if message[0][0].decode("utf-8") == ONLINE_STREAM:
                        dumped_data = message[0][1][0][1][b"v"].decode("utf-8")
                        event = "event: status\n"
                    else:
                        dumped_data = json.dumps(
                            {"new_message_id": last_id_returned.decode("utf-8")}
                        )
                        event = "event: new-notification\n"
                    event += f"data: {dumped_data}\n\n"
                    events_count += 1
                    logging.info(f"{connection_id}: Sent events. {events_count}")
                    yield event
                else:
                    event = "event: heartbeat\n"
                    event += "data: ping\n\n"
                    events_count += 1
                    logging.info(f"{connection_id}: Sending heartbeats")
                    yield event

        except asyncio.CancelledError:
            logging.info(f"{connection_id}: Disconnected after events. {events_count}")
            await listener.send_status_to_stream(
                message=OnlineStatus(user=connection_id, status="offline")
            )
            raise

    return StreamingHttpResponse(streamed_events(), content_type="text/event-stream")


@view_basicauth
@require_http_methods(["GET"])
async def get_new_posts(
    request: HttpRequest, last_id_returned: str, *args, **kwargs
):
    messages = PostService()
    messages_from_stream = await messages.get_messages_from_stream(
        last_id_returned=last_id_returned
    )
    messages_from_stream.reverse()
    messages = []
    for ele in messages_from_stream:
        print(ele[1][b"v"])
        data = DataToSend(**json.loads(ele[1][b"v"]))
        messages.append(
            {
                "name": data.account,
                "content": data.content,
                "created_at": data.created_at,
            }
        )
    return render(
        request,
        "streams/new_posts.html",
        context={"messages": messages},
    )
