import requests
import json

def test_deepseek_api():
    """Test DeepSeek API connection and response"""
    api_key = "sk-e60e809905e245b6ad290433c0064cf2"
    url = "https://api.deepseek.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Simple test request
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'API test successful' in JSON format: {\"status\": \"success\", \"message\": \"API test successful\"}"}
        ],
        "max_tokens": 50,
        "temperature": 0.1
    }
    
    try:
        print("Testing DeepSeek API...")
        response = requests.post(url, headers=headers, json=data, timeout=15)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"API Response: {content}")
            return True
        else:
            print(f"API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Exception: {e}")
        return False

if __name__ == "__main__":
    test_deepseek_api()
