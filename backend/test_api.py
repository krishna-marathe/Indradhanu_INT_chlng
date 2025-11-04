import requests
import json

def test_api():
    print("🧪 Testing Indradhanu Analytics API...")
    
    # Test home endpoint
    print("\n1️⃣ Testing home endpoint...")
    response = requests.get("http://127.0.0.1:5000/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Test file upload
    print("\n2️⃣ Testing file upload...")
    with open("../analytics_engine/data/sample_env_data.csv", "rb") as f:
        files = {"file": f}
        response = requests.post("http://127.0.0.1:5000/upload", files=files)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ {data['message']}")
        print(f"📊 Processed {data['rows']} rows, {data['columns']} columns")
        print(f"📈 Generated {len(data['charts'])} charts")
        print("💡 Key Insights:")
        for insight in data['insights']:
            print(f"   - {insight}")
    else:
        print(f"❌ Error: {response.text}")

if __name__ == "__main__":
    test_api()