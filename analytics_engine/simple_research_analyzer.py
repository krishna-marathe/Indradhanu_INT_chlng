import re
import os

def extract_text(file_path):
    """Extract readable text from PDF, DOCX, or TXT files."""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        try:
            import fitz  # PyMuPDF
            print(f"📖 Opening PDF with PyMuPDF...")
            text = ""
            with fitz.open(file_path) as doc:
                print(f"📄 PDF has {len(doc)} pages")
                for page_num, page in enumerate(doc):
                    page_text = page.get_text("text")
                    print(f"   Page {page_num + 1}: {len(page_text)} characters")
                    text += page_text
            print(f"✅ PDF extraction complete: {len(text)} total characters")
            return text
        except ImportError as e:
            error_msg = f"Error: PyMuPDF not installed. Run: pip install pymupdf. Details: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg
        except Exception as e:
            error_msg = f"Error reading PDF: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg
    
    elif ext == ".docx":
        try:
            import docx
            doc = docx.Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs])
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
    """Analyze research paper with simple keyword-based approach."""
    try:
        print(f"🔍 Analyzing file: {file_path}")
        
        # Extract text
        text = extract_text(file_path)
        
        print(f"📄 Extracted text length: {len(text)} characters")
        
        if text.startswith("Error:") or text.startswith("Unsupported"):
            print(f"❌ Extraction error: {text}")
            return {"error": text}
        
        if not text.strip():
            print(f"❌ No text found in document")
            return {"error": "No readable text found in document"}
        
        # Clean text
        cleaned = re.sub(r'\s+', ' ', text.strip())
        words = cleaned.split()
        word_count = len(words)
        
        # Simple region detection
        regions = []
        region_keywords = [
            'Maharashtra', 'India', 'Pune', 'Nashik', 'Mumbai', 'Delhi', 'Aurangabad', 'Solapur',
            'Asia', 'Europe', 'America', 'China', 'USA', 'Brazil', 'Australia', 'Africa'
        ]
        for region in region_keywords:
            if region in text:
                regions.append(region)
        
        # Year extraction
        year_matches = re.findall(r'20\d{2}', cleaned)
        years = sorted(list(set(year_matches)))
        
        # Climate keyword detection
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
        
        # Research method detection
        research_methods = []
        methods = [
            'statistical analysis', 'regression', 'machine learning', 'remote sensing',
            'modeling', 'simulation', 'survey', 'interview', 'field study', 'experiment'
        ]
        for method in methods:
            if method.lower() in text_lower:
                research_methods.append(method)
        
        # Trend extraction
        key_trends = []
        trend_patterns = [
            r'\d+\.?\d*°C',  # Temperature
            r'\d+\.?\d*%',   # Percentages
            r'\d+\.?\d*\s*mm',  # Rainfall
            r'\d+\.?\d*\s*days?',  # Days
            r'\d+\.?\d*\s*years?',  # Years
            r'\d+\.?\d*\s*km',  # Distance
        ]
        for pattern in trend_patterns:
            matches = re.findall(pattern, cleaned, re.IGNORECASE)
            key_trends.extend(matches[:5])
        
        # Generate summary
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
            r'(conclusion|findings?|results?)[\s:]*([^.]{50,200})',
            r'(we found|we observed|we conclude)[\s]*([^.]{30,150})',
            r'(significant|important|notable)[\s]*([^.]{30,120})'
        ]
        for pattern in finding_patterns:
            matches = re.findall(pattern, cleaned, re.IGNORECASE)
            for match in matches[:2]:
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