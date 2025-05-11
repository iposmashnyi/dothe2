from fastapi import FastAPI
from app.routers import tasks, quadrants

app = FastAPI()
app.include_router(tasks.router)
app.include_router(quadrants.quadrant_router)


@app.get("/")
async def root():
    return {"message": "Hello from Dothe2!"}
