from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

chatbot = pipeline("text-generation", model="microsoft/DialoGPT-medium")
# "openai-community/gpt2"
# "microsoft/DialoGPT-small"
# "microsoft/DialoGPT-large"

@app.route('/')
def home():
    return "Welcome to the ChatBot API"

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("user_input")
    response = chatbot(user_input, max_length=50, num_return_sequences=1)
    return jsonify({"response": response[0]["generated_text"]})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
