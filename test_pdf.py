#!/usr/bin/env python3
"""
Simple test script to verify PDF processing functionality
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, '/Users/jancoa/projects/responsibleAI')

try:
    from mcp_server import extract_pdf_text
    import fitz
    
    print("🧪 Testing PDF processing functionality...")
    
    # Create a simple test PDF
    doc = fitz.open()
    page = doc.new_page()
    
    test_content = """Test Academic Article

Abstract
This is a test paper to verify our PDF processing system works correctly.

Introduction
Academic papers require careful text extraction to preserve meaning and structure.

Methods
We use PyMuPDF for robust PDF text extraction.

Results
The system successfully processes academic content.

Conclusion
PDF processing functionality is working as expected."""
    
    page.insert_text((50, 50), test_content)
    
    # Save test PDF
    test_file = "test_academic_paper.pdf"
    doc.save(test_file)
    doc.close()
    
    print(f"✅ Created test PDF: {test_file}")
    
    # Test our extraction function
    result = extract_pdf_text(test_file)
    
    if result["success"]:
        print("✅ PDF text extraction successful!")
        print(f"📊 Extracted {result['total_chars']} characters from {result['total_pages']} pages")
        print(f"📄 Preview: {result['full_text'][:200]}...")
        
        # Test metadata extraction
        if result["metadata"]["title"]:
            print(f"📝 Title: {result['metadata']['title']}")
        else:
            print("📝 No title found in metadata")
            
    else:
        print(f"❌ PDF extraction failed: {result['error']}")
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"🧹 Cleaned up {test_file}")
    
    print("\n🎉 PDF processing test completed successfully!")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()