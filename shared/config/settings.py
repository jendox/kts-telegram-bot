from dataclasses import dataclass

from yaml import safe_load

from shared.broker.factory import BrokerType

__all__ = (
    "BrokerConfig",
    "Config",
    "load_config",
)


@dataclass
class BrokerConfig:
    type: BrokerType


@dataclass
class Config:
    broker: BrokerConfig


def load_config(config_path: str) -> Config:
    with open(config_path, "r") as file:
        data = safe_load(file)

        config = Config(
            BrokerConfig(
                type=BrokerType(data["broker"]["type"])
            )
        )

        return config
