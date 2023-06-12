import streamlit as st
import requests
from google.cloud import storage

st.set_page_config(page_title="Toxicity Classifier", page_icon="🤖")

model_list = [
    "logistic_regression",
    "decision_tree",
    "random_forest",
    "naive_bayes",
    "svm",
    "knn",
    "gradient_boosting",
    "xgboost",
    "catboost",
    "mlp",
    "ada_boost",
]

st.title("🤖 Toxicity Classifier")
st.divider()
st.image("https://nohatespeech.network/wp-content/uploads/2020/10/cropped-No-Hate-Speech-Logo-Transperent-1-1.png", width=600)
st.write("Please select a model and enter a sentence for **toxicity classification**.")

# Select a model
model = st.selectbox("🔍 Select a model:", model_list)

# Sentence input
sentence = st.text_input("📝 Enter a sentence:")

# Predict button
button = st.button("Predict")

if button:
    if sentence:
        st.write(f"🔄 Predicting...")
        response = requests.get(f"https://toxicity-classifier-cwkm3of3qa-ew.a.run.app/predict?sentence={sentence}&model={model}")
        toxic = response.json()

        # Display prediction
        st.markdown(f"**🔮 Prediction:** `{'Toxic' if toxic['y_pred'] == 1 else 'Unbiased'}`")
        st.markdown(f"**📊 Probabilities:** `{toxic['y_proba']}`")
    else:
        st.write("⚠️ Please enter a sentence.")
