#!/usr/bin/env python3

import sys
sys.path.append('.')

from analytics_engine.research_paper_analyzer import analyze_research_paper

def test_analyzer():
    try:
        result = analyze_research_paper('backend/sample_research_paper.txt')
        
        print("✅ Research Paper Analysis Test Results:")
        print(f"📍 Regions found: {len(result.get('regions', []))}")
        print(f"   Regions: {result.get('regions', [])[:5]}")  # First 5
        
        print(f"🔬 Research methods: {len(result.get('research_methods', []))}")
        print(f"   Methods: {result.get('research_methods', [])}")
        
        print(f"🌍 Climate keywords: {len(result.get('climate_keywords', []))}")
        print(f"   Keywords: {result.get('climate_keywords', [])[:5]}")  # First 5
        
        print(f"📊 Key trends: {len(result.get('key_trends', []))}")
        print(f"   Trends: {result.get('key_trends', [])[:5]}")  # First 5
        
        print(f"📅 Years: {result.get('years', [])}")
        print(f"📄 Word count: {result.get('word_count', 0)}")
        print(f"🎯 Confidence: {result.get('analysis_confidence', 'unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_analyzer()