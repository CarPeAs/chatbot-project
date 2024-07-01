from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
# "microsoft/DialoGPT-medium"
# "microsoft/DialoGPT-large"

# Historial de conversación inicializado vacío
chat_history_ids = None


@app.route('/')
def home():
    return "Welcome to the ChatBot API"

@app.route('/chat', methods=['POST'])
def chat():
    global chat_history_ids
    user_input = request.json.get("user_input")

   # Tokenizar la entrada del usuario y añadir el token de fin de secuencia (EOS)
    new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    
    # Concatenar el historial de conversación con la nueva entrada
    bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if chat_history_ids is not None else new_user_input_ids

    # Generar la respuesta limitando la longitud total de la conversación a 1000 tokens
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    
    # Decodificar la respuesta del bot y eliminar el token EOS
    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
