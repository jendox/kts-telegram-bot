import asyncio
import logging
from logging import getLogger

from poller import TelegramPoller
from shared.config import load_config

logger = getLogger(__name__)


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


async def main():
    setup_logging()
    poller = None

    try:
        config = load_config("shared/config/config.yaml")
        poller = TelegramPoller(config.broker.type)
        await poller.start()
        await poller.waiting_for_shutdown()
    except Exception as e:
        logger.error("Unexpected error: %s", e)
    finally:
        if poller:
            await poller.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Received KeyboardInterruption, shutting down...")
