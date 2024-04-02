ARG PYTHON_VERSION=3.9.6
FROM python:${PYTHON_VERSION}-slim as base

COPY ./app /app
COPY ./entrypoint.sh /entrypoint.sh
COPY ./requirements.txt /requirements.txt


RUN apt-get update && \
    apt-get install -y \
        tesseract-ocr \
    && python3 -m pip install -r requirements.txt \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*


RUN chmod +x entrypoint.sh

WORKDIR /app

# Run the application.
CMD [ "./entrypoint.sh" ]
# CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]