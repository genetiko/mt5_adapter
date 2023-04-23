import datetime
import struct
from typing import List

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse, Response
from starlette.responses import StreamingResponse

from terminals.config import settings
from terminals.drivers import Terminals
from terminals.models import SourceModel, InstrumentModel
from terminals.storage import get_sources, insert_instruments, get_instruments, get_instrument
from terminals.storage import insert_sources

app = FastAPI()
app.add_middleware(GZipMiddleware)

terminals = Terminals()


@app.on_event('startup')
async def startup_event():
    insert_sources([dict(name=t.name, server=t.server) for t in settings.terminals])

    id_mapping = {t.name: t.id for t in get_sources()}

    terminals.initialize([t + {'id': id_mapping[t.name]} for t in settings.terminals])

    for source_id, driver in terminals.terminals().items():
        insert_instruments([i | {'source_id': source_id} for i in (await driver.instruments())])


@app.on_event("shutdown")
async def shutdown_event():
    await terminals.shutdown()


@app.get('/sources', response_model=List[SourceModel])
async def sources():
    return get_sources()


@app.get('/instruments/{source_id}', response_model=List[InstrumentModel])
async def instruments(source_id: int):
    return get_instruments(source_id)


@app.get('/data/{instrument_id}')
async def instrument(instrument_id: int, instrument_type: str, start_time: datetime.datetime,
                     end_time: datetime.datetime) -> Response:
    instrument = get_instrument(instrument_id)
    source_id = instrument.source_id
    result = await terminals.get(source_id).instrument_data(instrument.name, instrument_type, start_time, end_time)

    if instrument_type == 'tick':
        pack_string = '<Qffif'
        # pack_string = '<QffiB'
    else:
        pack_string = '<QffffiiB'

    def stream():
        for index, row in enumerate(result):
            yield struct.pack(pack_string, *row)

    return StreamingResponse(stream())


@app.get('/chunks')
async def chunks(instrument_type: str, start_time: datetime.datetime, end_time: datetime.datetime,
                 frequency: str = "H"):
    ranges = pd.Series(pd.date_range(start_time, end_time, freq=frequency))
    pairs = list(zip(ranges[0::1], ranges[1::1]))
    return pairs


@app.get('/source_state')
async def source_state(source_id: int) -> JSONResponse:
    return JSONResponse(content=[])

# if __name__ == '__main__':
#     uvicorn.run("app:app", host='0.0.0.0', port=8888, reload=True)
