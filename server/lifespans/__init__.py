from asyncio import gather
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from server.lifespans.create_redis_index import create_redis_index
from server.lifespans.download_embeddings import download_embeddings


@asynccontextmanager
async def lifespans(_: FastAPI) -> AsyncGenerator[None, None]:
    """
    Summary
    -------
    the FastAPI lifespan function
    """
    await gather(
        download_embeddings(),
        create_redis_index()
    )

    yield
