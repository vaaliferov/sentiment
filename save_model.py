# pip3 install torch tensorflow transformers
from transformers import TFAutoModelForSequenceClassification

MODEL_NAME = 'Tatyana/rubert-base-cased-sentiment-new'
model = TFAutoModelForSequenceClassification.from_pretrained(MODEL_NAME, from_pt=True)
model.save_pretrained('model', saved_model=True)
