import datetime
import struct

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse, Response

from terminals.drivers import Terminals

app = FastAPI()
app.add_middleware(GZipMiddleware)


@app.on_event('startup')
async def startup_event():
    terminals = Terminals()
    terminals.initialize()


@app.post('/sources')
async def sources() -> JSONResponse:
    return JSONResponse(content=[{'id': 0}])


@app.post('/instruments')
async def instruments(source_id: int) -> JSONResponse:
    return JSONResponse(content=[{}])


@app.post('/instrument')
async def instrument(instrument_id: int, instrument_type: str, date: datetime.datetime) -> Response:
    source_id = 0  # Нужно получить источник по инструменту. Это можно по базе сделать.
    result = await Terminals.get()[instrument_id].instrument_data(instrument_id, instrument_type, date)
    # Пакуем все в бинарный поток.
    if instrument_type == 'tick':
        pack_string = '<QffffB'
        pack_size = struct.calcsize(pack_string)
        number_of_rows = len(result)
        buffer = bytearray(pack_size * number_of_rows)
        for index, row in enumerate(result):
            struct.pack_into(pack_string, buffer, index * pack_size, *row)
        return Response(content=buffer, media_type='application/octet-stream')

    # Здесь нужно добавить аналогично для рейтов, а не тиков.
    return Response(content=[])


@app.post('/chunks')
async def chunks(instrument_id: int, instrument_type: str, start_time: datetime.datetime,
                 end_time: datetime.datetime) -> JSONResponse:
    return JSONResponse(content=[])


@app.post('/source_state')
async def source_state(source_id: int) -> JSONResponse:
    return JSONResponse(content=[])


if __name__ == '__main__':
    uvicorn.run("app:app", host='0.0.0.0', port=8888, reload=True)
