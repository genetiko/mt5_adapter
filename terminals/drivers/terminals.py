from typing import Any, Dict

from terminals.drivers.driver import Driver
from .mt5_driver import MetaTrader5Driver


class Terminals:
    def __init__(self):
        self.__terminals: Dict[int, Driver] = {}

    def initialize(self, configuration):
        self.__terminals = dict([(config.id, MetaTrader5Driver(config)) for config in configuration])

    def __synchronize(self):
        ...

    async def shutdown(self):
        for terminal in self.__terminals.values():
            await terminal.shutdown()

    def __reset(self):
        ...

    def get(self, terminal_id) -> Driver:
        return self.__terminals[terminal_id]

    def terminals(self) -> dict[int, Driver]:
        return self.__terminals

    def terminal_descriptors(self):
        ...

    def is_terminal_active(self):
        ...

    def terminal_info(self, terminal_id: int) -> Dict[str, Any]:
        ...
