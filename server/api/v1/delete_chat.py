from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis

from server.api.v1 import v1
from server.dependencies import get_redis_client


@v1.get('/{chat_id}/delete_chat', deprecated=True)
async def delete_chat(
    chat_id: str,
    redis: Annotated[Redis, Depends(get_redis_client)],
):
    """
    Summary
    -------
    the `/delete_chat` route provides an endpoint for deleting a chat
    """
    for key in redis.scan_iter():  # type: ignore
        tag = await redis.hget(key, 'tag')  # type: ignore
        if tag == chat_id:
            redis.delete(key)  # type: ignore
