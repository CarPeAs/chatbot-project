from flask import Blueprint, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Cargar variables de entorno
# load_dotenv()

chat = Blueprint('chat', __name__)

# Proximo > Configuración de MongoDB
# mongo_uri = os.getenv("MONGODB_URI")
# client = MongoClient(mongo_uri)
# db = client['chatbot_db']
# conversations = db['conversations']

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
# "microsoft/DialoGPT-medium"
# "microsoft/DialoGPT-large"

# Historial de conversación inicializado vacío
chat_history_ids = None

@chat.route('/', methods=['POST'])
def chat_route():
    global chat_history_ids
    user_input = request.json.get("user_input")

   # Tokenizar la entrada del usuario y añadir el token de fin de secuencia (EOS)
    new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    
    # Concatenar el historial de conversación con la nueva entrada
    bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if chat_history_ids is not None else new_user_input_ids

    # Generar la máscara de atención
    attention_mask = torch.ones(bot_input_ids.shape, dtype=torch.long)

    # Generar la respuesta limitando la longitud total de la conversación a 100 tokens
    chat_history_ids = model.generate(bot_input_ids, attention_mask=attention_mask, max_length=100, pad_token_id=tokenizer.eos_token_id)
    
    # Decodificar la respuesta del bot y eliminar el token EOS
    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    # Proximo > almacenar conversación en MongoDB
    # conversations.insert_one({"user_input": user_input, "response": response})

    return jsonify({"response": response})


