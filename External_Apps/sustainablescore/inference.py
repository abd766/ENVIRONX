import requests
import json

# Replace with your actual Hugging Face API key
HUGGINGFACE_API_KEY = "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"

def run_inference(prompt):
    url = 'https://api-inference.huggingface.co/models/gpt2'
    headers = {
        'Authorization': f'Bearer {HUGGINGFACE_API_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        "inputs": prompt + ' Also add pros and cons in JSON format.',
        "options": {"use_cache": False}
    }
    
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    # Check if the response contains generated text
    if isinstance(response_json, list) and len(response_json) > 0:
        try:
            return json.loads(response_json[0]['generated_text'])
        except json.JSONDecodeError:
            return "Error: Could not decode JSON from response."
    else:
        return "Error: Unable to get a valid response."

