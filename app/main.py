from fastapi import FastAPI, HTTPException, Body, status, Query, Response
from pydantic import BaseModel
from typing import Optional, Annotated
# from src.worker import ocr_task
# from src.models import OCRRequest, OCRResponseSync, OCRResponseAsync
from redis import Redis
from rq import Queue
from rq.job import Job
from rq.exceptions import NoSuchJobError


app = FastAPI()
# redis_conn = Redis()
redis_conn = Redis(host='redis', port=6379, db=0)
q = Queue(connection=redis_conn)


@app.get("/",)
def imgsync():

    return {"Hello": "World"}