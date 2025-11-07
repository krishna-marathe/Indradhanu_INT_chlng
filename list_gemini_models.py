import requests

API_KEY = "AIzaSyA4IX7we2BPAuvKTRgHZjf1E1zomexttBM"

print("🔍 Listing available Gemini models...\n")

try:
    response = requests.get(
        f"https://generativelanguage.googleapis.com/v1/models?key={API_KEY}",
        timeout=10
    )
    
    if response.status_code == 200:
        data = response.json()
        models = data.get('models', [])
        
        print(f"✅ Found {len(models)} models:\n")
        
        for model in models:
            name = model.get('name', 'Unknown')
            display_name = model.get('displayName', 'Unknown')
            supported_methods = model.get('supportedGenerationMethods', [])
            
            if 'generateContent' in supported_methods:
                print(f"✅ {name}")
                print(f"   Display Name: {display_name}")
                print(f"   Methods: {', '.join(supported_methods)}")
                print()
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Exception: {str(e)}")
