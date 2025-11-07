#!/usr/bin/env python3

analyzer_code = '''def analyze_research_paper(file_path):
    """Simple research paper analyzer for testing."""
    import os
    import re
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        
        words = text.split()
        word_count = len(words)
        
        # Simple region detection
        regions = []
        region_keywords = ['Maharashtra', 'India', 'Pune', 'Nashik', 'Mumbai', 'Delhi', 'Asia', 'Europe', 'America']
        for region in region_keywords:
            if region in text:
                regions.append(region)
        
        # Simple year extraction
        year_matches = re.findall(r'20\\d{2}', text)
        years = sorted(list(set(year_matches)))
        
        # Climate keyword detection
        climate_keywords = []
        keywords = ['climate change', 'temperature', 'rainfall', 'drought', 'agriculture', 'global warming', 'precipitation']
        for keyword in keywords:
            if keyword.lower() in text.lower():
                climate_keywords.append(keyword)
        
        # Research method detection
        research_methods = []
        methods = ['statistical analysis', 'regression', 'machine learning', 'remote sensing', 'modeling']
        for method in methods:
            if method.lower() in text.lower():
                research_methods.append(method)
        
        # Key trends extraction
        key_trends = []
        trend_patterns = [r'\\d+\\.\\d+°C', r'\\d+%', r'\\d+ days?', r'\\d+ years?']
        for pattern in trend_patterns:
            matches = re.findall(pattern, text)
            key_trends.extend(matches[:3])
        
        # Generate summary
        summary_parts = []
        if regions:
            summary_parts.append(f"This research focuses on {', '.join(regions[:2])}")
        else:
            summary_parts.append("This research document")
        
        if years:
            if len(years) > 1:
                summary_parts.append(f"covering {years[0]} to {years[-1]}")
            else:
                summary_parts.append(f"from {years[0]}")
        
        summary = '. '.join(summary_parts) + f". Contains {word_count:,} words."
        
        return {
            "summary": summary,
            "regions": regions[:10],
            "years": years[:10],
            "word_count": word_count,
            "climate_keywords": climate_keywords[:10],
            "research_methods": research_methods[:8],
            "key_findings": ["Climate impacts on agriculture identified"] if "climate" in text.lower() and "agriculture" in text.lower() else [],
            "document_type": "research paper",
            "analysis_confidence": "high" if word_count > 1000 else "medium" if word_count > 500 else "low",
            "key_trends": key_trends[:15],
            "decades": [],
            "preview": text[:500] + "..." if len(text) > 500 else text
        }
        
    except Exception as e:
        return {"error": str(e)}
'''

# Write to file
with open('analytics_engine/research_paper_analyzer.py', 'w', encoding='utf-8') as f:
    f.write(analyzer_code)

print("✅ Research paper analyzer created successfully!")