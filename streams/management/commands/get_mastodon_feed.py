import json
import logging
import os
import urllib
from dataclasses import asdict

import httpx
import redis
from django.conf import settings
from django.core.management.base import BaseCommand
from httpx_sse import connect_sse

from streams.external import POST_STREAM, DataToSend

logger = logging.getLogger(__name__)
MASTODON_BEARER_TOKEN = os.getenv("MASTODON_BEARER_TOKEN")


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--domain",
            type=str,
            help="Provide the domain that you want to stream",
        )

    def handle(self, *args, **options):
        url = urllib.parse.urljoin(options["domain"], "/api/v1/streaming/public")
        headers = {"Authorization": f"Bearer {MASTODON_BEARER_TOKEN}"}
        logging.info(f"Connecting to :{url} and sending messages to {POST_STREAM}")

        connection_pool = redis.ConnectionPool.from_url(url=settings.REDIS_DSN)
        connection = redis.Redis(connection_pool=connection_pool)

        with httpx.Client() as client:
            with connect_sse(client, "GET", url=url, headers=headers) as event_source:
                for sse in event_source.iter_sse():
                    try:
                        data = json.loads(sse.data)
                    except Exception as ex:
                        logger.error("%s: %s" % (ex, sse.data))
                        logger.error("!" * 10)
                        continue
                    if sse.event == "update":
                        if not data["sensitive"]:
                            print(data)
                            message = DataToSend(
                                account=data["account"]["acct"],
                                content=data["content"],
                                created_at=data["created_at"],
                            )
                            connection.xadd(
                                name=POST_STREAM,
                                fields={"v": json.dumps(asdict(message))},
                            )
                            logger.info("#" * 10)
