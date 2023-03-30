import asyncio
from multiprocessing import Pipe, Process
from typing import Any, Dict, Optional

from terminals.drivers.driver import Driver
from .mt5_terminal_methods import TerminalInstance


class MetaTrader5Driver(Driver):
    def __init__(self, configuration: Dict[str, Any]):
        super().__init__()
        self.__configuration = configuration
        self.__lock = asyncio.Lock()
        self.__out_pipe, self.__in_pipe = Pipe(duplex=True)
        self.__process = Process(target=TerminalInstance.process, args=(configuration, self.__out_pipe, self.__in_pipe))
        self.__process.start()

    def __del__(self):
        self.__process.terminate()

    def restart(self):
        if self.__process is not None:
            self.__process.terminate()
        self.__out_pipe, self.__in_pipe = Pipe(duplex=True)
        self.__process = Process(target=TerminalInstance.process,
                                 args=(self.__configuration, self.__out_pipe, self.__in_pipe))
        self.__process.start()

    async def __request(self, message: Dict[str, Any]) -> Any:
        async with self.__lock:
            self.__out_pipe.send(message)
            is_data_available = self.__in_pipe.poll(timeout=self.__configuration['ping_timeout'])
            if is_data_available:
                return self.__in_pipe.recv()
            return None

    async def terminal_info(self) -> Optional[Dict[str, Any]]:
        return await self.__request({'cmd': 'get_terminal_info', })

    async def instruments(self):
        pass

    async def instrument_data(self):
        pass
