import json
import requests
import numpy as np
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoConfig

MODEL_NAME = 'Tatyana/rubert-base-cased-sentiment-new'
MODEL_URL = 'http://model:8501/v1/models/model:predict'

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
config = AutoConfig.from_pretrained(MODEL_NAME)
app = Flask(__name__, static_url_path='')

@app.route('/sentiment')
def get_sentiment():
    text = request.args.get('text')
    data = {'instances': [dict(tokenizer(text))]}
    r = requests.post(MODEL_URL, data=json.dumps(data))
    result = json.loads(r.text)['predictions'][0]
    label = config.id2label[np.argmax(result)]
    return jsonify({'label': label})
