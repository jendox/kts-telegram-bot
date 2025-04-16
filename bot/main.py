import asyncio
import logging
from logging import getLogger

from bot.core.manager import BotManager
from shared.config import load_config

logger = getLogger(__name__)


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


async def main():
    setup_logging()
    bot_manager = None

    try:
        config = load_config("shared/config/config.yaml")
        bot_manager = BotManager(config)
        await bot_manager.start()
        await bot_manager.waiting_for_shutdown()
    except Exception as e:
        logger.error("Unexpected error: %s", e)
    finally:
        if bot_manager:
            await bot_manager.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Received KeyboardInterruption, shutting down...")
