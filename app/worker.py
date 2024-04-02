import base64
import io
from PIL import Image
import pytesseract
import spacy
from textblob import TextBlob

nlp = spacy.load("en_core_web_sm")

def ocr_task(data):

    if "base64," in data:
        data = data.split("base64,")[-1]

    # Perform OCR
    img_data = base64.b64decode(data)
    image = Image.open(io.BytesIO(img_data))
    text = pytesseract.image_to_string(image)

    # Perform Named Entity Recognition
    entities = ner_task(text)

    # Perform Sentiment Analysis
    sentiment_polarity, sentiment_subjectivity = sentiment_analysis(text)

    return text, entities, sentiment_polarity, sentiment_subjectivity


def ner_task(text):

    # Perform Named Entity Recognition on the OCR text
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    return entities


def sentiment_analysis(text):

    # Perform Sentiment Analysis on the OCR text
    blob = TextBlob(text)
    sentiment_polarity = blob.sentiment.polarity
    sentiment_subjectivity = blob.sentiment.subjectivity

    return sentiment_polarity, sentiment_subjectivity