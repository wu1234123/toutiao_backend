from fastapi import FastAPI
from routers import news,users
from fastapi.middleware.cors import CORSMiddleware

from utils.exception_handlers import register_exception_handlers
from routers import favorite
from routers import history


app = FastAPI()

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def root():
    return {"message":"Hello world"}


app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)
