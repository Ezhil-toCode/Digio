# GiG

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

# from digio.web_services import faculty_routers
from digio.web_services import digio_routers, idcard_routers

app = FastAPI(name="digio")

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# This will get triggered as long as the
# output size is greater than 500 bytes.
# you can customize by adding an argument minimum_size=1000
# which will increase it to 1000 bytes
app.add_middleware(GZipMiddleware)

# app.include_router(faculty_routers.router)

app.include_router(digio_routers.router)
app.include_router(idcard_routers.router)
