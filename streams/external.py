import json
import logging
from dataclasses import asdict, dataclass
from functools import cache

import redis.asyncio as aredis
from django.conf import settings

logger = logging.getLogger(__name__)

STREAM_MESSAGE_PREFIX = "realtime-qa:"
POST_STREAM = "post-stream"
ONLINE_STREAM = "online-qa"
LISTEN_TIMEOUT = 5000 * 3


@dataclass
class DataToSend:
    account: str
    content: str
    created_at: str


@dataclass
class OnlineStatus:
    user: str
    status: str


@cache
def get_async_client() -> aredis.Redis:
    return aredis.from_url(settings.REDIS_DSN)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AsyncRedisConnectionFactory(metaclass=Singleton):
    """A singleton instance for redis connections"""

    def __init__(self, max_connections=2**31):
        logger.info("Connecting to redis using a connection pool")
        self.connection_pool = aredis.ConnectionPool.from_url(
            url=settings.REDIS_DSN, max_connections=max_connections
        )

    async def get_connection(self):
        return aredis.Redis(connection_pool=self.connection_pool)


class PostService:
    def __init__(self, connection_factory=AsyncRedisConnectionFactory) -> None:
        self.connection_factory = connection_factory()


    async def listen(
        self, stream_name: str, last_id_returned: str, timeout=LISTEN_TIMEOUT
    ):
        logger.info("Fetching from stream")
        aredis = await self.connection_factory.get_connection()
        if not last_id_returned:
            last_id_returned = "$"
        return await aredis.xread(
            count=1, streams={stream_name: last_id_returned}, block=timeout
        )

    async def get_messages_from_stream(
        self,
        last_id_returned: str,
    ):
        aredis = await self.connection_factory.get_connection()
        logger.info(f"{POST_STREAM} {last_id_returned}")
        if not last_id_returned:
            return await aredis.xrevrange(POST_STREAM, "+", "-", count=10)
        else:
            return await aredis.xrange(POST_STREAM, f"{last_id_returned}", "+")

    async def send_status_to_stream(
        self,
        message: OnlineStatus,
    ):
        aredis = await self.connection_factory.get_connection()
        await aredis.xadd(name=ONLINE_STREAM, fields={"v": json.dumps(asdict(message))})
        logger.info(f"Sent message to {ONLINE_STREAM}: {message}")

    async def listen_on_multiple_streams(
        self,
        last_id_returned: str,
        timeout=LISTEN_TIMEOUT,
    ):
        logger.info("Fetching from stream")
        aredis = await self.connection_factory.get_connection()
        if not last_id_returned:
            last_id_returned = "$"
        return await aredis.xread(
            count=1,
            streams={
                POST_STREAM: last_id_returned,
                ONLINE_STREAM: last_id_returned,
            },
            block=timeout,
        )
