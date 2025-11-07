import requests
import json

# Test the Gemini API with the new key
API_KEY = "AIzaSyA4IX7we2BPAuvKTRgHZjf1E1zomexttBM"
API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent"

def test_api():
    print("🧪 Testing Gemini API...")
    
    payload = {
        "contents": [{
            "parts": [{
                "text": "Hello! Please respond with 'API connection successful' if you can read this."
            }]
        }]
    }
    
    try:
        response = requests.post(
            f"{API_URL}?key={API_KEY}",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'No response')
            print(f"✅ SUCCESS!\n\nAI Response:\n{ai_response}")
            return True
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        return False

def test_climate_query():
    print("\n🌍 Testing Climate Query...")
    
    prompt = """You are an AI Climate Expert Assistant for the Indradhanu Climate Intelligence Platform.
Provide clear, data-driven insights on weather, crops, environmental conditions, climate trends, and disaster preparedness.
Keep your answers concise, factual, and user-friendly.

User question: What are the ideal weather conditions for rice cultivation in Maharashtra?"""
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    try:
        response = requests.post(
            f"{API_URL}?key={API_KEY}",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'No response')
            print(f"✅ CLIMATE QUERY SUCCESS!\n\nAI Response:\n{ai_response}")
            return True
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("GEMINI API TEST")
    print("=" * 60)
    
    # Test 1: Basic API connection
    test1 = test_api()
    
    # Test 2: Climate-specific query
    test2 = test_climate_query()
    
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    print(f"Basic API Test: {'✅ PASSED' if test1 else '❌ FAILED'}")
    print(f"Climate Query Test: {'✅ PASSED' if test2 else '❌ FAILED'}")
    print("=" * 60)
