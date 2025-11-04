"""
Comprehensive test script to verify all backend APIs
Tests upload, analysis, and visuals endpoints
"""
import requests
import json
import os
import time

def create_sample_csv():
    """Create a sample CSV file for testing"""
    sample_data = """Date,Temperature,Humidity,AQI,Location,Weather
2023-01-01,25.5,60,45,Delhi,Sunny
2023-01-02,26.0,58,42,Delhi,Cloudy
2023-01-03,24.8,62,48,Delhi,Rainy
2023-01-04,27.2,55,40,Mumbai,Sunny
2023-01-05,25.9,59,44,Mumbai,Cloudy
2023-01-06,28.1,52,38,Mumbai,Sunny
2023-01-07,23.5,65,50,Bangalore,Rainy
2023-01-08,24.2,63,47,Bangalore,Cloudy
2023-01-09,26.8,57,43,Bangalore,Sunny
2023-01-10,25.0,61,46,Chennai,Humid"""
    
    with open('sample.csv', 'w') as f:
        f.write(sample_data)
    print("✅ Created sample.csv")

def test_health_check():
    """Test the health check endpoint"""
    print("\n🔍 Testing health check endpoint...")
    try:
        response = requests.get('http://127.0.0.1:5000/')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Message: {data.get('message', 'N/A')}")
            print("✅ Health check PASSED")
            return True
        else:
            print("❌ Health check FAILED")
            return False
    except Exception as e:
        print(f"❌ Health check ERROR: {str(e)}")
        return False

def test_upload():
    """Test file upload endpoint"""
    print("\n📤 Testing file upload...")
    
    if not os.path.exists('sample.csv'):
        create_sample_csv()
    
    try:
        url = 'http://127.0.0.1:5000/upload'
        
        with open('sample.csv', 'rb') as f:
            files = {'file': ('sample.csv', f, 'text/csv')}
            response = requests.post(url, files=files, timeout=30)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ Upload SUCCESS!")
                print(f"   Filename: {data.get('filename', 'N/A')}")
                print(f"   Rows: {data.get('rows', 'N/A')}")
                print(f"   Columns: {data.get('columns', 'N/A')}")
                print(f"   Charts: {len(data.get('charts', []))}")
                print(f"   Insights: {len(data.get('insights', []))}")
                return data.get('filename')
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {str(e)}")
                print(f"Raw response: {response.text[:500]}...")
                return None
        else:
            print(f"❌ Upload FAILED with status {response.status_code}")
            print(f"Response: {response.text[:500]}...")
            return None
            
    except Exception as e:
        print(f"❌ Upload ERROR: {str(e)}")
        return None

def test_visuals():
    """Test visuals listing endpoint"""
    print("\n🖼️ Testing visuals endpoint...")
    try:
        response = requests.get('http://127.0.0.1:5000/visuals/')
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            file_count = data.get('count', 0)
            print(f"✅ Visuals endpoint SUCCESS!")
            print(f"   Files found: {file_count}")
            if file_count > 0:
                print(f"   Sample files: {data.get('files', [])[:3]}")
            return True
        else:
            print(f"❌ Visuals FAILED with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Visuals ERROR: {str(e)}")
        return False

def test_report(filename):
    """Test analysis report endpoint"""
    if not filename:
        print("\n⚠️ Skipping report test - no filename available")
        return False
        
    print(f"\n📊 Testing report endpoint for {filename}...")
    try:
        url = f'http://127.0.0.1:5000/report/{filename}'
        response = requests.get(url, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ Report endpoint SUCCESS!")
                report = data.get('report', {})
                print(f"   Dataset info: {report.get('dataset_info', {})}")
                return True
            except json.JSONDecodeError as e:
                print(f"❌ Report JSON decode error: {str(e)}")
                return False
        else:
            print(f"❌ Report FAILED with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Report ERROR: {str(e)}")
        return False

def test_uploads_list():
    """Test uploads listing endpoint"""
    print("\n📋 Testing uploads list endpoint...")
    try:
        response = requests.get('http://127.0.0.1:5000/uploads')
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Uploads list SUCCESS!")
            print(f"   Total uploads: {len(data)}")
            return True
        else:
            print(f"❌ Uploads list FAILED with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Uploads list ERROR: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting comprehensive backend API tests...")
    print("=" * 60)
    
    # Track test results
    results = {
        'health_check': False,
        'upload': False,
        'visuals': False,
        'report': False,
        'uploads_list': False
    }
    
    # Run tests
    results['health_check'] = test_health_check()
    
    uploaded_filename = test_upload()
    results['upload'] = uploaded_filename is not None
    
    results['visuals'] = test_visuals()
    results['report'] = test_report(uploaded_filename)
    results['uploads_list'] = test_uploads_list()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY:")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"   {test_name.replace('_', ' ').title()}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Backend is fully functional.")
    else:
        print("⚠️ Some tests failed. Check the logs above for details.")
    
    # Cleanup
    if os.path.exists('sample.csv'):
        os.remove('sample.csv')
        print("\n🧹 Cleaned up test files")

if __name__ == "__main__":
    main()