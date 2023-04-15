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
        self.__parent_pipe, self.__child_pipe = Pipe(duplex=True)
        self.__process = Process(target=TerminalInstance.process, args=(configuration, self.__child_pipe))
        self.__process.start()

    def __del__(self):
        self.__process.terminate()

    def restart(self):
        if self.__process is not None:
            self.__process.terminate()
        self.__parent_pipe, self.__child_pipe = Pipe(duplex=True)
        self.__process = Process(target=TerminalInstance.process,
                                 args=(self.__configuration, self.__child_pipe))
        self.__process.start()

    async def __request(self, message: Dict[str, Any]) -> Any:
        async with self.__lock:
            self.__parent_pipe.send(message)
            is_data_available = self.__parent_pipe.poll(timeout=self.__configuration['ping_timeout'])
            if is_data_available:
                return self.__parent_pipe.recv()
            return None

    async def terminal_info(self) -> Optional[Dict[str, Any]]:
        return await self.__request({'cmd': 'get_terminal_info'})

    async def instruments(self):
        return await self.__request({'cmd': 'get_instruments_info'})

    async def instrument_data(self, instrument, instrument_type, start_time, end_time):
        return await self.__request({
            'cmd': 'get_instrument_data',
            'parameters': {
                'instrument': instrument,
                'instrument_type': instrument_type,
                'start': start_time,
                'end': end_time
            }
        })

    async def shutdown(self):
        await self.__request({'cmd': 'terminate'})
        self.__del__()
