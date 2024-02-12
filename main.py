from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import config
from routes.Api import router as api_router
from config.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["http://localhost:8000", config.config().API_URL,
        config.config().CLIENT_SIDE_URL]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)