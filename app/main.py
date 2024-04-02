from fastapi import FastAPI, HTTPException, Body, status, Query, Response
from pydantic import BaseModel
from typing import Optional, Annotated
from app.worker import ocr_task
from app.models import OCRRequest, OCRResponseSync, OCRResponseAsync
from redis import Redis
from rq import Queue
from rq.job import Job
from rq.exceptions import NoSuchJobError


app = FastAPI()
# redis_conn = Redis()
redis_conn = Redis(host='redis', port=6379, db=0)
q = Queue(connection=redis_conn)


@app.post("/imgsync", response_model=OCRResponseSync)
def imgsync(request: OCRRequest):

    # Perform OCR, NER, and Sentiment Analysis on the image synchronously
    text, entities, sentiment_polarity, sentiment_subjectivity = ocr_task(request.data)

    return {
        "text": text,
        "entities": entities,
        "sentiment_polarity": sentiment_polarity,
        "sentiment_subjectivity": sentiment_subjectivity,
    }


@app.post("/imgasync", response_model=OCRResponseAsync)
async def imgsync(request: OCRRequest):
    data = request.data

    # Enqueue the OCR task to be processed asynchronously
    job = q.enqueue(ocr_task, data)
    job_id = str(job.get_id())

    return {
            "job_id": job_id,
            "status": "scheduled",
        }

@app.get("/result/{job_id}", response_model=OCRResponseAsync)
async def get_result(job_id: str):

    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except NoSuchJobError:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.is_finished:
        text, entities, sentiment_polarity, sentiment_subjectivity = job.result
        result = {
            "text": text,
            "entities": entities,
            "sentiment_polarity": sentiment_polarity,
            "sentiment_subjectivity": sentiment_subjectivity,
        }
        return {
            "job_id": job_id,
            "status": "completed",
            "result": result,
        }
    else:
        return {
            "job_id": job_id,
            "status": "pending",
        }