from transformers import pipeline

# Inicializando o modelo de NLP da biblioteca Transformers
def generate_suggestions(response):
    # Carregar pipeline de linguagem natural
    nlp = pipeline("text-generation", model="gpt2")  # Modelo leve para demonstração

    # Prompt base para sugerir frases baseadas na resposta
    prompt = (
        "Given the user's response: '" + response +
        "', suggest 3 helpful conversational tips or responses for improving English."
    )

    # Gerar sugestões usando o modelo
    generated = nlp(prompt, max_length=100, num_return_sequences=1, truncation=True)

    # Processar a saída para extrair sugestões
    raw_text = generated[0]['generated_text']

    # Dividir sugestões baseadas em delimitadores ou formatação
    suggestions = [
        suggestion.strip() for suggestion in raw_text.split('\n') if suggestion.strip()
    ]

    # Retornar no máximo 3 sugestões úteis
    return suggestions[:3]

# Exemplo de chamada
response = "I think English grammar is confusing."
print(generate_suggestions(response))
