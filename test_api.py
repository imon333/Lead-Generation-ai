import requests
import json

def test_search_api():
    """Test the search API endpoint"""
    url = "http://localhost:8000/api/search"
    payload = {
        "query": "Software Engineer",
        "title": "CTO",
        "location": "San Francisco",
        "sources": ["linkedin"]
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Results:")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Lead Generation API...")
    test_search_api() 