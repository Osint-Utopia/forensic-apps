from openai import OpenAI

client = OpenAI(api_key="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",
base_url="https://openrouter.ai/api/v1")

chat = client.chat.completions.create(
    model="deepseek/deepseek-r1:free",
    messages=[
        { 
        "role":"user",
        "content":"dame un diccionario actualizado de etiquetas y terminos de html"
        }
    ]
)

print(chat.choices[0].message.content)

