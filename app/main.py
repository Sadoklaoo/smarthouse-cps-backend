from fastapi import FastAPI
from app.workers.celery_worker import add

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Smart House API is running!"}

@app.post("/trigger_add/")
async def trigger_add(x: int, y: int):
    task = add.delay(x, y)
    return {"task_id": task.id}