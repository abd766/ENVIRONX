import streamlit as st
import requests
from bs4 import BeautifulSoup

def analyze_amazon_product(product_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(product_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'lxml')

        title = soup.find('span', {'id': 'productTitle'})
        if title:
            title_text = title.get_text(strip=True)
            return title_text
        else:
            return None, "Product title not found."
    except requests.exceptions.RequestException as e:
        return None, f"Error fetching data: {str(e)}"

def check_sustainability_with_openai(product_title):
    api_key=''
    # Replace with your OpenAI API key
    url = 'https://api.openai.com/v1/chat/completions'
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': f"Is the product '{product_title}' environmentally sustainable?"}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        return response_json['choices'][0]['message']['content']
    except Exception as e:
        return f"Error checking sustainability: {str(e)}"

st.title("Amazon Product Environmental Analysis")

# Input for product URL
product_url = st.text_input("Enter the Amazon product URL:")

if st.button("Analyze"):
    if product_url:
        title = analyze_amazon_product(product_url)
        if title:
            sustainability_status = check_sustainability_with_openai(title)
            st.write(f"**Product Title:** {title}")
            st.write(f"**Sustainability Status:** {sustainability_status}")
        else:
            st.write(title)
    else:
        st.warning("Please enter a valid Amazon product URL.")
