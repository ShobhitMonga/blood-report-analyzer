import os
import requests
import json

api_key = os.getenv("GEMINI_API_KEY")
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
response = requests.get(url)
models = response.json().get('models', [])
for m in models:
    if 'gemini' in m.get('name', '').lower():
        print(f"Name: {m.get('name')} | generateContent: {'generateContent' in m.get('supportedGenerationMethods', [])}")
