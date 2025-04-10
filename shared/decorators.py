import asyncio
import functools
import logging


def retry_async(
        retries: int = 5,
        delay: float = 2.0,
        allowed_exceptions: tuple = (Exception,),
        logger: logging.Logger = None
):
    """Декоратор для повторной попытки асинхронной функции в случае исключения.
    :param retries: Количество попыток
    :param delay: Задержка между попытками в секундах
    :param allowed_exceptions: Исключения, при которых делать retry
    :param logger: Логгер (по умолчанию используется logging.getLogger)
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
                        f"Attempt {attempt}/{retries} failed for {func.__name__}: {e}"
                    )
                    if attempt == retries:
                        _logger.error(f"Function {func.__name__} failed after {retries} attempts.")
                        raise
                    await asyncio.sleep(delay)

        return wrapper

    return decorator
