#!/usr/bin/env python3

analyzer_code = '''import re
import os

def extract_text(file_path):
    """Extract readable text from PDF, DOCX, or TXT files."""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        try:
            import fitz  # PyMuPDF
            text = ""
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text("text")
            return text
        except ImportError:
            return "Error: PyMuPDF not installed. Run: pip install pymupdf"
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    
    elif ext == ".docx":
        try:
            import docx
            doc = docx.Document(file_path)
            return "\\n".join([p.text for p in doc.paragraphs])
        except ImportError:
            return "Error: python-docx not installed. Run: pip install python-docx"
        except Exception as e:
            return f"Error reading DOCX: {str(e)}"
    
    elif ext == ".txt":
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            return f"Error reading TXT: {str(e)}"
    
    else:
        return f"Unsupported file type: {ext}"

def analyze_research_paper(file_path):
    """Analyze research paper and return structured insights with proper text extraction."""
    try:
        # Extract text using proper method based on file type
        text = extract_text(file_path)
        
        # Check if extraction was successful
        if text.startswith("Error:") or text.startswith("Unsupported"):
            return {"error": text}
        
        if not text.strip():
            return {"error": "No readable text found in document"}
        
        # Clean text
        cleaned = re.sub(r'\\s+', ' ', text.strip())
        words = cleaned.split()
        word_count = len(words)
        
        # Enhanced region detection with spaCy if available
        regions = []
        try:
            import spacy
            nlp = spacy.load("en_core_web_sm")
            doc = nlp(cleaned[:10000])  # Limit to first 10k chars for performance
            regions = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]
            regions = list(set(regions))  # Remove duplicates
        except:
            # Fallback to keyword-based detection
            region_keywords = ['Maharashtra', 'India', 'Pune', 'Nashik', 'Mumbai', 'Delhi', 'Asia', 'Europe', 'America', 'China', 'USA', 'Brazil', 'Australia']
            for region in region_keywords:
                if region in text:
                    regions.append(region)
        
        # Enhanced year extraction
        year_matches = re.findall(r'20\\d{2}', cleaned)
        years = sorted(list(set(year_matches)))
        
        # Enhanced climate keyword detection
        climate_keywords = []
        keywords = [
            'climate change', 'global warming', 'temperature', 'rainfall', 'precipitation',
            'drought', 'agriculture', 'crop yield', 'greenhouse gas', 'carbon dioxide',
            'sea level', 'glacier', 'biodiversity', 'ecosystem', 'deforestation'
        ]
        text_lower = cleaned.lower()
        for keyword in keywords:
            if keyword in text_lower:
                climate_keywords.append(keyword)
        
        # Enhanced research method detection
        research_methods = []
        methods = [
            'statistical analysis', 'regression', 'machine learning', 'remote sensing',
            'modeling', 'simulation', 'survey', 'interview', 'field study', 'experiment'
        ]
        for method in methods:
            if method.lower() in text_lower:
                research_methods.append(method)
        
        # Enhanced trend extraction
        key_trends = []
        trend_patterns = [
            r'\\d+\\.?\\d*°C',  # Temperature
            r'\\d+\\.?\\d*%',   # Percentages
            r'\\d+\\.?\\d*\\s*mm',  # Rainfall
            r'\\d+\\.?\\d*\\s*days?',  # Days
            r'\\d+\\.?\\d*\\s*years?',  # Years
            r'\\d+\\.?\\d*\\s*km',  # Distance
        ]
        for pattern in trend_patterns:
            matches = re.findall(pattern, cleaned, re.IGNORECASE)
            key_trends.extend(matches[:5])  # Limit per pattern
        
        # Generate intelligent summary
        summary_parts = []
        
        if regions:
            summary_parts.append(f"This research focuses on {', '.join(regions[:3])}")
        else:
            summary_parts.append("This research document")
        
        if years:
            if len(years) > 1:
                summary_parts.append(f"covering the period from {years[0]} to {years[-1]}")
            else:
                summary_parts.append(f"from the year {years[0]}")
        
        if climate_keywords:
            summary_parts.append(f"examining {', '.join(climate_keywords[:3])}")
        
        if research_methods:
            summary_parts.append(f"using {', '.join(research_methods[:2])} methodologies")
        
        summary = '. '.join(summary_parts) + f". The document contains {word_count:,} words."
        
        # Extract key findings
        key_findings = []
        finding_patterns = [
            r'(conclusion|findings?|results?)[\\s:]*([^.]{50,200})',
            r'(we found|we observed|we conclude)[\\s]*([^.]{30,150})',
            r'(significant|important|notable)[\\s]*([^.]{30,120})'
        ]
        for pattern in finding_patterns:
            matches = re.findall(pattern, cleaned, re.IGNORECASE)
            for match in matches[:2]:  # Limit findings
                if isinstance(match, tuple) and len(match) > 1:
                    finding = match[1].strip()
                    if len(finding) > 20:
                        key_findings.append(finding)
        
        # Determine confidence
        confidence = "high" if word_count > 1000 and regions else "medium" if word_count > 500 else "low"
        
        return {
            "summary": summary,
            "regions": regions[:10],
            "years": years[:10],
            "word_count": word_count,
            "climate_keywords": climate_keywords[:10],
            "research_methods": research_methods[:8],
            "key_findings": key_findings[:5],
            "document_type": "research paper",
            "analysis_confidence": confidence,
            "key_trends": list(set(key_trends))[:15],
            "decades": [],
            "preview": cleaned[:500] + "..." if len(cleaned) > 500 else cleaned
        }
        
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}
'''

# Write to file
with open('analytics_engine/research_paper_analyzer.py', 'w', encoding='utf-8') as f:
    f.write(analyzer_code)

print("✅ Fixed research paper analyzer created successfully!")
print(f"📄 File size: {len(analyzer_code)} bytes")