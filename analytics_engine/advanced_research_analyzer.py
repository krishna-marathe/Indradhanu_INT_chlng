import re
import os
from collections import Counter

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
            return f"Error: PyMuPDF not installed. Run: pip install pymupdf"
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    
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

def extract_sections(text):
    """Extract major sections from the research paper."""
    sections = {}
    
    # Common section patterns
    section_patterns = {
        'abstract': r'(?:abstract|summary)[\s:]*([^\n]{100,1000})',
        'introduction': r'(?:introduction|background)[\s:]*([^\n]{200,2000})',
        'methodology': r'(?:methodology|methods?|materials? and methods?)[\s:]*([^\n]{200,2000})',
        'results': r'(?:results?|findings?)[\s:]*([^\n]{200,2000})',
        'discussion': r'(?:discussion|analysis)[\s:]*([^\n]{200,2000})',
        'conclusion': r'(?:conclusion|summary|concluding remarks?)[\s:]*([^\n]{100,1000})'
    }
    
    for section_name, pattern in section_patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
        if matches:
            sections[section_name] = matches[0][:500]  # Limit to 500 chars
    
    return sections

def analyze_methodology(text):
    """Detailed methodology analysis."""
    methodology = {
        'research_design': [],
        'data_collection': [],
        'analysis_techniques': [],
        'sample_info': [],
        'tools_used': []
    }
    
    # Research design patterns
    design_keywords = [
        'experimental', 'observational', 'longitudinal', 'cross-sectional',
        'qualitative', 'quantitative', 'mixed methods', 'case study',
        'comparative', 'descriptive', 'exploratory', 'explanatory'
    ]
    
    # Data collection methods
    collection_keywords = [
        'survey', 'questionnaire', 'interview', 'focus group', 'observation',
        'field study', 'laboratory', 'secondary data', 'primary data',
        'satellite data', 'remote sensing', 'sensor data', 'measurements'
    ]
    
    # Analysis techniques
    analysis_keywords = [
        'statistical analysis', 'regression', 'correlation', 'ANOVA', 't-test',
        'chi-square', 'factor analysis', 'cluster analysis', 'time series',
        'machine learning', 'neural network', 'random forest', 'SVM',
        'thematic analysis', 'content analysis', 'discourse analysis'
    ]
    
    # Tools and software
    tools_keywords = [
        'SPSS', 'R', 'Python', 'MATLAB', 'SAS', 'Stata', 'Excel',
        'QGIS', 'ArcGIS', 'NVivo', 'ATLAS.ti', 'TensorFlow', 'PyTorch'
    ]
    
    text_lower = text.lower()
    
    for keyword in design_keywords:
        if keyword.lower() in text_lower:
            methodology['research_design'].append(keyword)
    
    for keyword in collection_keywords:
        if keyword.lower() in text_lower:
            methodology['data_collection'].append(keyword)
    
    for keyword in analysis_keywords:
        if keyword.lower() in text_lower:
            methodology['analysis_techniques'].append(keyword)
    
    for keyword in tools_keywords:
        if keyword in text:  # Case-sensitive for tools
            methodology['tools_used'].append(keyword)
    
    # Extract sample size information
    sample_patterns = [
        r'(\d+)\s*(?:participants?|respondents?|subjects?|samples?)',
        r'sample size[:\s]*(\d+)',
        r'n\s*=\s*(\d+)'
    ]
    
    for pattern in sample_patterns:
        matches = re.findall(pattern, text_lower)
        if matches:
            methodology['sample_info'].extend(matches[:3])
    
    return methodology

def extract_key_findings(text):
    """Extract detailed key findings and results."""
    findings = []
    
    # Patterns for findings
    finding_patterns = [
        r'(?:we found|found that|results? show|demonstrated that|revealed that|indicated that)[\s:]*([^.]{50,300})',
        r'(?:significant|important|notable|key|major)[\s]+(?:finding|result|outcome|effect|impact|relationship|correlation)[\s:]*([^.]{50,300})',
        r'(?:conclusion|conclude that|concluded that)[\s:]*([^.]{50,300})',
        r'(?:evidence suggests?|data shows?|analysis reveals?)[\s:]*([^.]{50,300})',
        r'(?:increase|decrease|reduction|growth|decline)[\s]+(?:of|by|in)[\s]+(\d+\.?\d*\s*%?[^.]{20,200})'
    ]
    
    for pattern in finding_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches[:10]:  # Limit to 10 per pattern
            if isinstance(match, tuple):
                finding = match[0] if match[0] else match[1] if len(match) > 1 else ""
            else:
                finding = match
            
            finding = finding.strip()
            if len(finding) > 30 and finding not in findings:
                findings.append(finding)
    
    return findings[:15]  # Return top 15 findings

def analyze_statistical_data(text):
    """Extract and analyze statistical information."""
    stats = {
        'percentages': [],
        'p_values': [],
        'correlations': [],
        'sample_sizes': [],
        'confidence_intervals': [],
        'effect_sizes': []
    }
    
    # Extract percentages
    percentages = re.findall(r'\d+\.?\d*\s*%', text)
    stats['percentages'] = list(set(percentages))[:20]
    
    # Extract p-values
    p_values = re.findall(r'p\s*[<>=]\s*0\.\d+', text, re.IGNORECASE)
    stats['p_values'] = list(set(p_values))[:10]
    
    # Extract correlation coefficients
    correlations = re.findall(r'r\s*=\s*[+-]?0\.\d+', text, re.IGNORECASE)
    stats['correlations'] = list(set(correlations))[:10]
    
    # Extract sample sizes
    sample_sizes = re.findall(r'n\s*=\s*\d+', text, re.IGNORECASE)
    stats['sample_sizes'] = list(set(sample_sizes))[:5]
    
    # Extract confidence intervals
    ci_patterns = [
        r'95%\s*(?:CI|confidence interval)[:\s]*\[?([^\]]{10,50})\]?',
        r'CI\s*=\s*([^\n]{10,50})'
    ]
    for pattern in ci_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        stats['confidence_intervals'].extend(matches[:5])
    
    return stats

def identify_research_gaps(text):
    """Identify research gaps and limitations mentioned."""
    gaps = []
    
    gap_patterns = [
        r'(?:limitation|limited|gap|lack of|need for|future research|further study)[\s:]*([^.]{30,200})',
        r'(?:however|although|despite)[\s,]*([^.]{30,200})',
        r'(?:not yet|remains unclear|unknown|unexplored)[\s]*([^.]{30,200})'
    ]
    
    for pattern in gap_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches[:5]:
            if isinstance(match, tuple):
                gap = match[0]
            else:
                gap = match
            gap = gap.strip()
            if len(gap) > 20 and gap not in gaps:
                gaps.append(gap)
    
    return gaps[:8]

def extract_recommendations(text):
    """Extract recommendations and implications."""
    recommendations = []
    
    rec_patterns = [
        r'(?:recommend|recommendation|suggest|should|ought to|need to)[\s:]*([^.]{30,200})',
        r'(?:implication|policy|practice|application)[\s:]*([^.]{30,200})',
        r'(?:future research|further study|next steps?)[\s:]*([^.]{30,200})'
    ]
    
    for pattern in rec_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches[:5]:
            if isinstance(match, tuple):
                rec = match[0]
            else:
                rec = match
            rec = rec.strip()
            if len(rec) > 20 and rec not in recommendations:
                recommendations.append(rec)
    
    return recommendations[:10]

def generate_executive_summary(text, analysis_data):
    """Generate a comprehensive executive summary."""
    word_count = len(text.split())
    
    # Build multi-paragraph summary
    summary_parts = []
    
    # Part 1: Scope and Focus
    if analysis_data['regions']:
        regions_text = ', '.join(analysis_data['regions'][:5])
        summary_parts.append(f"This research paper examines {regions_text}")
    else:
        summary_parts.append("This research paper presents a comprehensive study")
    
    # Part 2: Temporal Coverage
    if analysis_data['years']:
        years = sorted(analysis_data['years'])
        if len(years) > 1:
            summary_parts.append(f"spanning the period from {years[0]} to {years[-1]}")
        else:
            summary_parts.append(f"focusing on the year {years[0]}")
    
    # Part 3: Research Focus
    if analysis_data['climate_keywords']:
        keywords = ', '.join(analysis_data['climate_keywords'][:4])
        summary_parts.append(f"with particular emphasis on {keywords}")
    
    # Part 4: Methodology
    if analysis_data['methodology']['analysis_techniques']:
        methods = ', '.join(analysis_data['methodology']['analysis_techniques'][:3])
        summary_parts.append(f"The study employs {methods}")
    
    # Part 5: Sample and Data
    if analysis_data['methodology']['sample_info']:
        sample = analysis_data['methodology']['sample_info'][0]
        summary_parts.append(f"analyzing data from {sample} observations")
    
    # Part 6: Key Findings
    if analysis_data['key_findings']:
        summary_parts.append(f"The research reveals {len(analysis_data['key_findings'])} significant findings")
    
    # Part 7: Document Stats
    summary_parts.append(f"The document comprises {word_count:,} words across {len(text.split(chr(12)))} sections")
    
    return '. '.join(summary_parts) + '.'

def analyze_research_paper(file_path):
    """Comprehensive research paper analysis with in-depth insights."""
    try:
        print(f"🔍 Starting comprehensive analysis of: {file_path}")
        
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
        
        print(f"📊 Analyzing {word_count} words...")
        
        # Extract sections
        sections = extract_sections(cleaned)
        
        # Basic extractions
        regions = []
        region_keywords = [
            'Maharashtra', 'India', 'Pune', 'Nashik', 'Mumbai', 'Delhi', 'Bangalore',
            'Asia', 'Europe', 'America', 'Africa', 'China', 'USA', 'Brazil', 'Australia',
            'Pakistan', 'Bangladesh', 'Nepal', 'Sri Lanka', 'Indonesia', 'Thailand'
        ]
        for region in region_keywords:
            if region in text:
                regions.append(region)
        
        # Extract years
        year_matches = re.findall(r'20\d{2}|19\d{2}', cleaned)
        years = sorted(list(set(year_matches)))
        
        # Climate keywords
        climate_keywords = []
        keywords = [
            'climate change', 'global warming', 'temperature', 'rainfall', 'precipitation',
            'drought', 'flood', 'agriculture', 'crop yield', 'greenhouse gas', 'carbon dioxide',
            'sea level', 'glacier', 'biodiversity', 'ecosystem', 'deforestation',
            'sustainability', 'renewable energy', 'carbon footprint', 'emissions',
            'adaptation', 'mitigation', 'resilience', 'vulnerability', 'extreme weather'
        ]
        text_lower = cleaned.lower()
        for keyword in keywords:
            if keyword in text_lower:
                climate_keywords.append(keyword)
        
        # Detailed methodology analysis
        methodology = analyze_methodology(cleaned)
        
        # Extract key findings
        key_findings = extract_key_findings(cleaned)
        
        # Statistical analysis
        statistical_data = analyze_statistical_data(cleaned)
        
        # Research gaps
        research_gaps = identify_research_gaps(cleaned)
        
        # Recommendations
        recommendations = extract_recommendations(cleaned)
        
        # Prepare analysis data
        analysis_data = {
            'regions': regions,
            'years': years,
            'climate_keywords': climate_keywords,
            'methodology': methodology,
            'key_findings': key_findings,
            'statistical_data': statistical_data,
            'research_gaps': research_gaps,
            'recommendations': recommendations
        }
        
        # Generate executive summary
        executive_summary = generate_executive_summary(cleaned, analysis_data)
        
        # Determine confidence
        confidence_score = 0
        if word_count > 2000: confidence_score += 3
        elif word_count > 1000: confidence_score += 2
        elif word_count > 500: confidence_score += 1
        
        if len(regions) > 3: confidence_score += 2
        if len(years) > 5: confidence_score += 2
        if len(key_findings) > 5: confidence_score += 2
        if methodology['analysis_techniques']: confidence_score += 2
        
        if confidence_score >= 8:
            confidence = "high"
        elif confidence_score >= 5:
            confidence = "medium"
        else:
            confidence = "low"
        
        print(f"✅ Analysis complete: {len(key_findings)} findings, {len(regions)} regions")
        
        return {
            "executive_summary": executive_summary,
            "word_count": word_count,
            "sections_found": list(sections.keys()),
            "regions": regions[:15],
            "years": years[:20],
            "climate_keywords": climate_keywords[:15],
            "methodology": methodology,
            "key_findings": key_findings,
            "statistical_data": statistical_data,
            "research_gaps": research_gaps,
            "recommendations": recommendations,
            "document_type": "research paper",
            "analysis_confidence": confidence,
            "confidence_score": confidence_score,
            "preview": cleaned[:800] + "..." if len(cleaned) > 800 else cleaned
        }
        
    except Exception as e:
        print(f"❌ Analysis error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": f"Analysis failed: {str(e)}"}