import requests
import json

url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type': 'application/json',
}

conversation_history = []

full_prompt = "\n".join()

data = {
    "model": "llama3",
    "stream": False,
    "prompt": "Si tengo instalado en mi pc Ollama y quiero correrlo en mi gpu rtx 3050ti, Ollama correria en mi gpu o en mi cpu?",
}
response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    response_text = response.text
    data = json.loads(response_text)
    actual_response = data["response"]
    conversation_history.append(actual_response)
    print(actual_response)
else:
    print("Error:", response.status_code, response.text)