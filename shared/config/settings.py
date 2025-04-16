from dataclasses import dataclass

from yaml import safe_load

from shared.broker.factory import BrokerType

__all__ = (
    "BrokerConfig",
    "Config",
    "StorageConfig",
    "load_config",
)

from shared.storage.factory import StorageType


@dataclass
class BrokerConfig:
    type: BrokerType
    queue: str


@dataclass
class StorageConfig:
    type: StorageType


@dataclass
class Config:
    broker: BrokerConfig
    storage: StorageConfig


def load_config(config_path: str) -> Config:
    with open(config_path, "r") as file:
        data = safe_load(file)

        return Config(
            BrokerConfig(
                type=BrokerType(data["broker"]["type"]),
                queue=data["broker"]["queue"],
            ),
            StorageConfig(type=StorageType(data["storage"]["type"])),
        )
