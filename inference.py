

def predict(client, system_prompt, user_prompt):
    response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0.2, 
    max_tokens=400
    )
    return response.choices[0].message.content
