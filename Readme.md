OCR Service Documentation
-----------------------------------

### Overview

The OCR Service is a web application built using FastAPI that accepts base64_encoded_image, performs Optical Character Recognition (OCR) using tesseract, Named Entity Recognition (NER) using spacy, and Sentiment Analysis on the extracted text using textblob, and returns the results. The service provides both synchronous and asynchronous APIs to handle image processing.

### Building and running the application with Docker

1. Create a virtual environment:
`python3 -m venv .`
`source bin/activate`
2. Start the application by running:
`docker compose up --build`.
3. Restart the Docker containers:
`docker-compose up`
4. To stop and remove the containers:
`docker-compose down`

### Installation without Docker

#### Requirements

* Python 3.12.2
* Redis server
* RQ (Redis Queue) worker
* Linux OS

### Commands

1. Create a virtual environment:
`python3 -m venv venv`
`source venv/bin/activate`
2. Install the required packages:
`pip install -r requirements.txt`
3. Install the English language model for spacy:
`python -m spacy download en_core_web_sm`


#### Running the Service without Docker

1. Start the Redis server :
`redis-server`
2. Start the RQ worker in a separate terminal window:
`rq worker --url redis://localhost:6379/0`
3. Start the FastAPI application:
`uvicorn app.main:app --host 0.0.0.0 --port 8000`



The service will be available at `http://localhost:8000`.



### Using the API

The OCR Service provides the following endpoints:

#### Synchronous API

`POST http://localhost:8000/imgsync`

Accepts a base64-encoded image and returns the OCR text, named entities, sentiment polarity, and sentiment subjectivity.

Example requestBody:
{
  "data": "<base64_encoded_image>"
}
Example response:
{
  "text": "This is an example text extracted from the image.",
  "entities": [
    ["John Doe", "PERSON"],
    ["Apple Inc.", "ORG"]
  ],
  "sentiment_polarity": 0.5,
  "sentiment_subjectivity": 0.3
}

#### Asynchronous API

`POST http://localhost:8000/imgasync`

Accepts a base64-encoded image and returns a job_id. The image processing is performed in the background.

Example requestBody:
{
  "data": "<base64_encoded_image>"
}
Example response:
{
  "job_id": "123456789",
  "status": "scheduled"
}

`GET http://localhost:8000/results/{job_id}`

Accepts a job ID and returns the OCR text, named entities, sentiment polarity, and sentiment subjectivity for the base64-encoded image.

Example request:
`GET http://localhost:8000/result/123456789`
Example response:
{ 
  "job_id": "123456789",
  "status": "completed",
  result:
        {
          "text": "This is an example text extracted from the image.",
          "entities": [
            ["John Doe", "PERSON"],
            ["OCR Service", "ORG"]
          ],
          "sentiment_polarity": 0.5,
          "sentiment_subjectivity": 0.3
        }
}


#### Testing
To run the tests for the OCR service, follow these steps:

1. Run the synchronous tests:
`pytest app/test_endpoints.py::test_sync_endpoint`

2. Run the asynchronous tests:
`pytest app/test_endpoints.py::test_async_endpoint`

3. Run the synchronous and asynchronous tests both at a time:
`pytest`

To check the testcases at production:

1. Change the `ENDPOINT` variable with the api url at `app/conftest.py`