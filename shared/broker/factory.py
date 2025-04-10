import enum

from shared.broker.base import MessageBroker
from shared.broker.rabbitmq_broker import RabbitMQBroker

__all__ = (
    "BrokerType",
    "get_broker",
)


class BrokerType(enum.Enum):
    RabbitMQ = "rabbitmq"


def get_broker(broker_type: BrokerType) -> MessageBroker:
    if broker_type == BrokerType.RabbitMQ:
        return RabbitMQBroker()

    raise ValueError(f"Unsupported broker type: {broker_type.value}")
