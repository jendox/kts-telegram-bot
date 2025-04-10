import asyncio
import functools
import logging


def retry_async(
        retries: int = 5,
        delay: float = 2.0,
        allowed_exceptions: tuple = (Exception,),
        logger: logging.Logger | None = None,
):
    """Декоратор для повторной попытки асинхронной функции в случае исключения.

    Args:
        retries: количество попыток
        delay: задержка между попытками в секундах
        allowed_exceptions: исключения, при которых делать retry
        logger: логгер (по умолчанию используется logging.getLogger)
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            _logger = logger or logging.getLogger(func.__module__)
            for attempt in range(1, retries + 1):
                try:
                    return await func(*args, **kwargs)
                except allowed_exceptions as e:
                    _logger.warning(
                        "Attempt %s/%s failed for %s: %s",
                        attempt,
                        retries,
                        func.__name__,
                        e,
                    )
                    if attempt == retries:
                        _logger.error(
                            "Function %s failed after %s attempts.",
                            func.__name__,
                            retries,
                        )
                        raise
                    await asyncio.sleep(delay * attempt)

        return wrapper

    return decorator
