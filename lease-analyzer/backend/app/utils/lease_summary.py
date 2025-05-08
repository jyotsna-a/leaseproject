import openai

def generate_summary(text):
    prompt = f"Summarize this lease with key info (rent, deposit, utilities, pets, parking, risks, sublease):\n\n{text[:3000]}"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response["choices"][0]["message"]["content"]