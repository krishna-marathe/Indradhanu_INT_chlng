#!/usr/bin/env python3

print("Testing imports...")

try:
    import re
    print("✅ re imported")
except Exception as e:
    print(f"❌ re failed: {e}")

try:
    import os
    print("✅ os imported")
except Exception as e:
    print(f"❌ os failed: {e}")

try:
    import spacy
    print("✅ spacy imported")
except Exception as e:
    print(f"❌ spacy failed: {e}")

try:
    nlp = spacy.load("en_core_web_sm")
    print("✅ spacy model loaded")
except Exception as e:
    print(f"❌ spacy model failed: {e}")

print("\nTesting research paper analyzer...")

try:
    exec(open('analytics_engine/research_paper_analyzer.py').read())
    print("✅ File executed successfully")
    print("Functions available:", [name for name in locals() if callable(locals()[name]) and not name.startswith('_')])
except Exception as e:
    print(f"❌ File execution failed: {e}")
    import traceback
    traceback.print_exc()