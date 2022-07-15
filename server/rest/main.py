import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env")))

from rest.dependency import inject
from rest.router.binance_router import binance_router

app = FastAPI()
app.include_router(binance_router, tags=['Binance'])

# run on initial
@app.on_event("startup")
async def event_startup():
    await inject()
