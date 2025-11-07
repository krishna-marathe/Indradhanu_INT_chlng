"""
Test file upload to check for errors
"""
import requests

def test_upload():
    print("Testing file upload...")
    
    # Use a simple test CSV
    csv_content = """Year,Temperature,Rainfall
2020,25.5,100
2021,26.2,95
2022,26.8,110
2023,27.1,105"""
    
    # Create a file-like object
    files = {
        'file': ('test_data.csv', csv_content, 'text/csv')
    }
    
    try:
        print("Uploading file...")
        response = requests.post(
            'http://127.0.0.1:5000/upload',
            files=files,
            timeout=180
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
        if response.status_code == 200:
            print("✅ Upload successful!")
            return True
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_upload()
