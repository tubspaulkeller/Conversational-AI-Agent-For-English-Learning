import asyncio
import logging
from typing import Any


async def non_cancellable_shield(func) -> Any:
    logger = logging.getLogger(__name__)
    future = asyncio.ensure_future(func)
    try:
        # Shield task to prevent cancelling
        logger.info('Tries awaiting future')
        return await asyncio.shield(future)
    except asyncio.CancelledError:
        # Await original task
        logger.info('Shield cancelled')
        return await future
