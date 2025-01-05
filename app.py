from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db, Interaction
from services.grammar import correct_grammar
from services.sentiment import analyze_sentiment
from services.suggestions import generate_suggestions
from transformers import pipeline
import json  # Importa o módulo JSON para converter listas em strings

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Pipeline da IA
chat_pipeline = pipeline("text-generation", model="gpt2")

@app.before_request
def setup():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    user_input = request.json.get('input')
    if not user_input:
        return jsonify({"error": "Input is required."}), 400

    # Resposta da IA
    chat_response = chat_pipeline(user_input, max_length=50, num_return_sequences=1)[0]['generated_text']

    # Análise de sentimentos
    sentiment = analyze_sentiment(user_input)

    # Correção gramatical
    corrections = correct_grammar(user_input)

    # Sugestões
    suggestions = generate_suggestions(chat_response)

    # Converter sugestões para string (JSON)
    suggestions_str = json.dumps(suggestions)

    # Armazenar no banco de dados
    interaction = Interaction(
        user_input=user_input,
        response=chat_response,
        suggestions=suggestions_str,  # Armazena como string JSON
        sentiment=sentiment,
        grammar_corrections=json.dumps(corrections)  # Converter correções para string JSON também
    )
    db.session.add(interaction)
    db.session.commit()

    return jsonify({
        "response": chat_response,
        "sentiment": sentiment,
        "grammar_corrections": corrections,
        "suggestions": suggestions
    })

if __name__ == '__main__':
    app.run(debug=True)
