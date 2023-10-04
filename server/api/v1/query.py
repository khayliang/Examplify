from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis

from server.api.v1 import v1
from server.config import Config
from server.databases.redis import create_query_parameters
from server.databases.redis import redis_query as redis_query_helper
from server.dependencies import get_redis_client
from server.features import LLM, Embedding, question_answering
from server.schemas.v1 import Answer, Query


@v1.post('/{chat_id}/query')
async def query(
    chat_id: str,
    request: Query,
    redis: Annotated[Redis, Depends(get_redis_client)]
) -> Answer:
    """
    Summary
    -------
    the `/query` route provides an endpoint for performning retrieval-augmented generation
    """
    redis_query = redis_query_helper('tag', chat_id, request.top_k)

    redis_query_parameters = create_query_parameters(
        Embedding().encode_query(request.query)
    )

    search_response = await redis.ft(Config.redis_index_name).search(
        redis_query,
        redis_query_parameters  # type: ignore  (this is a bug in the redis-py library)
    )

    context = ' '.join(
        document['content'] for document
        in search_response.docs # type: ignore
    )

    return Answer(messages=question_answering(
        request.query,
        context,
        request.messages,
        LLM.query
    ))
