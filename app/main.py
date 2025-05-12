from fastapi import FastAPI
from app.api.v1 import quadrants, tasks

app = FastAPI()
app.include_router(tasks.router)
app.include_router(quadrants.router)


@app.get("/")
async def root():
    return {"message": "Hello from Dothe2!"}
