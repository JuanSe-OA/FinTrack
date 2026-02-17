from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.infraestructure.database.base import Base
from app.infraestructure.database.session import engine
import app.infraestructure.database.models  # IMPORTANTE

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)
