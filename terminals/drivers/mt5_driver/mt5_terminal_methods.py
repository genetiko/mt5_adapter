from collections import defaultdict
from datetime import datetime
from multiprocessing.connection import Connection
from typing import Any, Dict, List

import MetaTrader5


class TerminalInstance:
    __TICK_FLAGS_MAPPING = defaultdict(lambda: 0x00, {
        MetaTrader5.TICK_FLAG_BID: 0x01,
        MetaTrader5.TICK_FLAG_ASK: 0x02,
        MetaTrader5.TICK_FLAG_LAST: 0x04,
        MetaTrader5.TICK_FLAG_VOLUME: 0x08,
    })

    __PERIOD_MAPPING = {
        '1m': MetaTrader5.TIMEFRAME_M1,
        '2m': MetaTrader5.TIMEFRAME_M2,
        '3m': MetaTrader5.TIMEFRAME_M3,
        '4m': MetaTrader5.TIMEFRAME_M4,
        '5m': MetaTrader5.TIMEFRAME_M5,
        '6m': MetaTrader5.TIMEFRAME_M6,
        '10m': MetaTrader5.TIMEFRAME_M10,
        '12m': MetaTrader5.TIMEFRAME_M12,
        '15m': MetaTrader5.TIMEFRAME_M15,
        '20m': MetaTrader5.TIMEFRAME_M20,
        '30m': MetaTrader5.TIMEFRAME_M30,
        '1h': MetaTrader5.TIMEFRAME_H1,
        '2h': MetaTrader5.TIMEFRAME_H2,
        '3h': MetaTrader5.TIMEFRAME_H3,
        '4h': MetaTrader5.TIMEFRAME_H4,
        '6h': MetaTrader5.TIMEFRAME_H6,
        '8h': MetaTrader5.TIMEFRAME_H8,
        '12h': MetaTrader5.TIMEFRAME_H12,
        '1d': MetaTrader5.TIMEFRAME_D1,
        '1w': MetaTrader5.TIMEFRAME_W1,
        '1mn': MetaTrader5.TIMEFRAME_MN1,
    }

    @staticmethod
    def __initialize(configuration: Dict[str, Any]):
        MetaTrader5.initialize(server=configuration['server'],
                               login=configuration['login'],
                               password=configuration['password'])

    @staticmethod
    def __shutdown():
        MetaTrader5.shutdown()

    @staticmethod
    def __get_terminal_info() -> Dict[str, Any]:
        terminal_info = dict(MetaTrader5.terminal_info())
        account_info = dict(MetaTrader5.account_info())

        return {
            'name': terminal_info['name'],
            'company': terminal_info['company'],
            'server': account_info['server'],
        }

    @staticmethod
    def __get_instruments() -> List[Dict[str, Any]]:
        symbols = MetaTrader5.symbols_get()
        return [{
            'name': symbol.name,
            'path': symbol.path,
            'currency_base': symbol.currency_base,
            'currency_profit': symbol.currency_profit,
            'currency_margin': symbol.currency_margin,
            'description': symbol.description,
            'digits': symbol.digits,
            'volume_min': symbol.volume_min,
            'volume_max': symbol.volume_max,
            'volume_step': symbol.volume_step,
            'spread_floating': symbol.spread_float
        } for symbol in symbols]

    @staticmethod
    def __get_instrument_data(instrument: str, instrument_type: str, start: datetime, end: datetime) -> List:
        if instrument_type == 'tick':
            ticks = MetaTrader5.copy_ticks_range(instrument, start, end, MetaTrader5.COPY_TICKS_ALL)
            return [
                # timestamp bid ask volume flags
                [tick[0], tick[1], tick[2], tick[6],
                 tick[7]] for tick in ticks
                # TerminalInstance.__map_flags(tick[7])] for tick in ticks
            ]

        rates = MetaTrader5.copy_rates_range(instrument, TerminalInstance.__PERIOD_MAPPING[instrument_type], start, end)
        return [
            # timestamp open high low close tick_volume volume spread
            [rate[0], rate[1], rate[2], rate[3], rate[4], rate[5], rate[6], rate[7]] for rate in rates
        ]

    @staticmethod
    def __map_flags(flags: int) -> int:
        mapping = TerminalInstance.__TICK_FLAGS_MAPPING
        return mapping[flags & MetaTrader5.TICK_FLAG_BID] | mapping[flags & MetaTrader5.TICK_FLAG_ASK] | mapping[
            flags & MetaTrader5.TICK_FLAG_LAST] | mapping[flags & MetaTrader5.TICK_FLAG_VOLUME]

    @staticmethod
    def __cmd_terminate():
        TerminalInstance.__shutdown()

    @staticmethod
    def process(configuration: Dict[str, Any], pipe: Connection):
        TerminalInstance.__initialize(configuration)

        while True:
            message = pipe.recv()

            # Terminate.
            if message['cmd'] == 'terminate':
                break
            # Fetch terminal info.
            elif message['cmd'] == 'get_terminal_info':
                pipe.send(TerminalInstance.__get_terminal_info())
            # Fetch instruments info.
            elif message['cmd'] == 'get_instruments_info':
                pipe.send(TerminalInstance.__get_instruments())
            # Fetch instrument history data.
            elif message['cmd'] == 'get_instrument_data':
                parameters = message['parameters']
                pipe.send(TerminalInstance.__get_instrument_data(
                    parameters['instrument'],
                    parameters['instrument_type'],
                    parameters['start'],
                    parameters['end']
                ))

        TerminalInstance.__shutdown()
