import json
import requests
import telegram
import numpy as np
import telegram.ext
from secret import *
from transformers import AutoConfig
from transformers import AutoTokenizer

MODEL_NAME = 'Tatyana/rubert-base-cased-sentiment-new'
MODEL_URL = 'http://model:8501/v1/models/model:predict'

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
config = AutoConfig.from_pretrained(MODEL_NAME)

def handle_text(update, context):
    
    text = update.message.text
    user = update.message.from_user
    chat_id = update.message.chat_id
    
    if user['id'] != BOT_OWNER_ID:
        msg = f"@{user['username']} {user['id']}"
        context.bot.send_message(BOT_OWNER_ID, msg)
        context.bot.send_message(BOT_OWNER_ID, text)
    
    if text == '/start':
        usage = 'Please, send me a text in Russian'
        context.bot.send_message(chat_id, usage)
        return None
    
    data = {'instances': [dict(tokenizer(text))]}
    r = requests.post(MODEL_URL, data=json.dumps(data))
    result = json.loads(r.text)["predictions"][0]
    label = config.id2label[np.argmax(result)]
    context.bot.send_message(chat_id, label)

handler = telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_text)
updater = telegram.ext.Updater(BOT_TOKEN)
updater.dispatcher.add_handler(handler)
updater.start_polling()
updater.idle()
