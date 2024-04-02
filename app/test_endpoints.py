import pytest
import asyncio
import httpx
import base64
import aiofiles
import requests

from app.conftest import ENDPOINT, TEST_IMAGE_PATH, OCR_TEXT

@pytest.mark.parametrize(
    "image_path, ocr_text",
    [
        (TEST_IMAGE_PATH, OCR_TEXT),
    ],
)

def test_sync_endpoint(image_path, ocr_text):
    # convert image file to base64
    with open(image_path, "rb") as f:
        image_data = f.read()
    base64_encoded_image = base64.b64encode(image_data).decode()

    # Send a POST request to the sync endpoint with the base64-encoded image
    path = f"{ENDPOINT}/imgsync"
    response = requests.post(path, json={"data": base64_encoded_image})
    assert response.status_code == 200
    result = response.json()
    assert "text" in result
    assert "entities" in result
    assert "sentiment_polarity" in result
    assert "sentiment_subjectivity" in result
    assert result["text"] == ocr_text

@pytest.mark.asyncio
async def test_async_endpoint():
    async with httpx.AsyncClient() as client:

        # convert the image to base64
        async with aiofiles.open(TEST_IMAGE_PATH, "rb") as f:
            image_data = await f.read()
        base64_encoded_image = base64.b64encode(image_data).decode()

        # Send a POST request to the async endpoint with the base64-encoded image
        path = f"{ENDPOINT}/imgasync"
        response = await client.post(path, json={"data": base64_encoded_image})
        assert response.status_code == 200
        job_id = response.json()["job_id"]

        # Wait for the job to be processed
        await asyncio.sleep(5)

        # Get the results for the job
        path = f"{ENDPOINT}/result/{job_id}"
        response = await client.get(path)
        assert response.status_code == 200
        result = response.json()['result']
        assert "text" in result
        assert "entities" in result
        assert "sentiment_polarity" in result
        assert "sentiment_subjectivity" in result