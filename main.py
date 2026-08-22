from fastapi import FastAPI
from routers import news
app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Hello world"}


app.include_router(news.router)
