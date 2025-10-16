#!/usr/bin/env python3
"""
Setup script for Academic PDF Summarization MCP Server
Run this script to install dependencies and test the basic functionality.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    
    # Install MCP
    if not run_command("pip install mcp>=0.9.0", "Installing MCP framework"):
        return False
    
    # Install PyMuPDF
    if not run_command("pip install PyMuPDF>=1.23.0", "Installing PyMuPDF"):
        return False
    
    print("✅ All dependencies installed successfully!")
    return True

def test_imports():
    """Test that all required imports work."""
    print("\n🧪 Testing imports...")
    
    try:
        import mcp
        print("✅ MCP imported successfully")
    except ImportError as e:
        print(f"❌ MCP import failed: {e}")
        return False
    
    try:
        import fitz
        print("✅ PyMuPDF (fitz) imported successfully")
    except ImportError as e:
        print(f"❌ PyMuPDF import failed: {e}")
        return False
    
    return True

def test_pdf_processing():
    """Test basic PDF processing functionality."""
    print("\n📄 Testing PDF processing...")
    
    # Create a simple test PDF content
    try:
        import fitz
        
        # Create a simple test PDF
        doc = fitz.open()  # Create new PDF
        page = doc.new_page()
        
        # Add some test text
        text = """Academic Article Test
        
This is a test academic article for the PDF processing system.

Abstract
This paper presents a test case for PDF text extraction.

Introduction  
Academic papers often contain structured content that needs to be processed.

Methodology
We use PyMuPDF for text extraction from PDF documents.

Results
The system successfully extracts text from PDF files.

Conclusion
PDF processing works as expected for academic content."""
        
        page.insert_text((50, 50), text)
        
        # Save test PDF
        test_pdf_path = "test_article.pdf"
        doc.save(test_pdf_path)
        doc.close()
        
        print(f"✅ Created test PDF: {test_pdf_path}")
        
        # Test text extraction
        doc = fitz.open(test_pdf_path)
        text = doc[0].get_text()
        doc.close()
        
        if len(text.strip()) > 0:
            print(f"✅ Successfully extracted {len(text)} characters from test PDF")
            print(f"Preview: {text[:100]}...")
            return True
        else:
            print("❌ No text extracted from test PDF")
            return False
            
    except Exception as e:
        print(f"❌ PDF processing test failed: {e}")
        return False
    finally:
        # Clean up test file
        if os.path.exists("test_article.pdf"):
            os.remove("test_article.pdf")

def main():
    """Main setup function."""
    print("🚀 Academic PDF Summarization MCP Server Setup")
    print("=" * 50)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed during dependency installation")
        return False
    
    # Test imports
    if not test_imports():
        print("\n❌ Setup failed during import testing")
        return False
    
    # Test PDF processing
    if not test_pdf_processing():
        print("\n❌ Setup failed during PDF processing test")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run the MCP server: python mcp_server.py")
    print("2. Test with a real PDF file")
    print("3. Integrate with your AI assistant")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)