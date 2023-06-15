import logging
from simpletransformers.classification import ClassificationModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sklearn.feature_extraction.text import TfidfVectorizer
from fakenews.model import load_models
from fakenews.preprocess import preprocess_text
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import os

app = FastAPI()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Setting up application...")
app.state.model = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/reset")
def reset():
    """
    Reset the model.
    """
    logging.info("🧑‍💻 Resetting model...")
    app.state.model = None
    logging.info("✅ Model reset.")

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    roberta_dir = os.path.join(parent_dir, "models", "roberta")

    try:
        os.rmdir(roberta_dir)
    except OSError as e:
        logging.info(e)

    return {
        'status': 'ok'
    }


@app.get("/predict")
def predict(
        sentence: str
    ):
    """
    Make a single prediction.
    """
    logging.info("🧑‍💻 Making prediction...")

    X_preprocessed = preprocess_text(sentence)
    roberta = load_models()

    logging.info("✅ Model loaded.")

    y_pred = roberta.predict([sentence])[0]

    print(y_pred)

    logging.info("✅ Prediction made.")

    return y_pred[0]

    #json_compatible_item_data = jsonable_encoder(y_pred)
    #eturn JSONResponse(content=json_compatible_item_data)


@app.get("/")
def root():
    return {
        'API': '200 [GET /predict?sentence=hello]'
    }
