#!/usr/bin/env python3
"""
Academic PDF Summarization MCP Server
A Model Context Protocol server for processing and summarizing academic PDFs.
"""

import asyncio
import logging
from typing import Any, Dict, List
import base64
import tempfile
import os

# MCP imports
try:
    from mcp.server import Server
    from mcp.server.models import InitializationOptions
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    MCP_AVAILABLE = True
except ImportError:
    print("MCP not available. Install with: pip install mcp")
    MCP_AVAILABLE = False

# PDF processing
try:
    import fitz  # PyMuPDF
    PDF_AVAILABLE = True
except ImportError:
    print("PyMuPDF not available. Install with: pip install PyMuPDF")
    PDF_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check dependencies
if not MCP_AVAILABLE:
    logger.error("MCP framework not available. Please install with: pip install mcp")
    exit(1)

if not PDF_AVAILABLE:
    logger.error("PyMuPDF not available. Please install with: pip install PyMuPDF")
    exit(1)

# Initialize MCP server
server = Server("academic-pdf-summarizer")

def extract_pdf_text(pdf_path: str) -> Dict[str, Any]:
    """
    Extract text content from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary containing extracted text and metadata
    """
    try:
        # Open PDF document
        doc = fitz.open(pdf_path)
        
        extracted_data = {
            "success": True,
            "pages": [],
            "total_pages": doc.page_count,
            "full_text": "",
            "metadata": {}
        }
        
        # Extract metadata
        metadata = doc.metadata
        extracted_data["metadata"] = {
            "title": metadata.get("title", "").strip(),
            "author": metadata.get("author", "").strip(),
            "subject": metadata.get("subject", "").strip(),
            "creator": metadata.get("creator", "").strip(),
            "producer": metadata.get("producer", "").strip(),
        }
        
        # Extract text from each page
        full_text_parts = []
        for page_num in range(doc.page_count):
            page = doc[page_num]
            page_text = page.get_text()
            
            if page_text.strip():  # Only add non-empty pages
                page_data = {
                    "page_number": page_num + 1,
                    "text": page_text,
                    "char_count": len(page_text)
                }
                extracted_data["pages"].append(page_data)
                full_text_parts.append(page_text)
        
        # Combine all text
        extracted_data["full_text"] = "\n\n".join(full_text_parts)
        extracted_data["total_chars"] = len(extracted_data["full_text"])
        
        # Store page count before closing
        page_count = doc.page_count
        doc.close()
        logger.info(f"Successfully extracted text from {page_count} pages")
        
        return extracted_data
        
    except Exception as e:
        logger.error(f"Error extracting PDF text: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "pages": [],
            "total_pages": 0,
            "full_text": "",
            "metadata": {}
        }

def save_base64_to_temp_file(base64_data: str, filename: str = "temp_pdf.pdf") -> str:
    """
    Save base64 encoded data to a temporary file.
    
    Args:
        base64_data: Base64 encoded file data
        filename: Temporary filename
        
    Returns:
        Path to the temporary file
    """
    try:
        # Decode base64 data
        file_data = base64.b64decode(base64_data)
        
        # Create temporary file
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, filename)
        
        with open(temp_path, 'wb') as f:
            f.write(file_data)
            
        logger.info(f"Saved base64 data to temporary file: {temp_path}")
        return temp_path
        
    except Exception as e:
        logger.error(f"Error saving base64 to temp file: {str(e)}")
        raise

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="process_pdf_article",
            description="Extract text content from an academic PDF article for analysis",
            inputSchema={
                "type": "object",
                "properties": {
                    "pdf_data": {
                        "type": "string",
                        "description": "Base64 encoded PDF file data"
                    },
                    "filename": {
                        "type": "string", 
                        "description": "Original filename of the PDF (optional)",
                        "default": "article.pdf"
                    }
                },
                "required": ["pdf_data"]
            }
        ),
        Tool(
            name="extract_pdf_text",
            description="Basic PDF text extraction tool for testing",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Local file path to PDF (for testing)"
                    }
                },
                "required": ["file_path"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent]:
    """Handle MCP tool calls."""
    
    if name == "process_pdf_article":
        try:
            pdf_data = arguments.get("pdf_data")
            filename = arguments.get("filename", "article.pdf")
            
            if not pdf_data:
                return [TextContent(
                    type="text",
                    text="Error: No PDF data provided"
                )]
            
            # Save base64 data to temporary file
            temp_path = save_base64_to_temp_file(pdf_data, filename)
            
            # Extract text from PDF
            result = extract_pdf_text(temp_path)
            
            # Clean up temporary file
            try:
                os.unlink(temp_path)
            except Exception:
                pass  # Ignore cleanup errors
            
            if result["success"]:
                response = f"""# PDF Text Extraction Results

## Document Metadata
- **Title**: {result['metadata'].get('title', 'Not available')}
- **Author**: {result['metadata'].get('author', 'Not available')}
- **Pages**: {result['total_pages']}
- **Total Characters**: {result['total_chars']:,}

## Extracted Text Preview
{result['full_text'][:1000]}{'...' if len(result['full_text']) > 1000 else ''}

## Processing Summary
Successfully extracted text from {len(result['pages'])} pages.
"""
            else:
                response = f"Error processing PDF: {result['error']}"
                
            return [TextContent(type="text", text=response)]
            
        except Exception as e:
            logger.error(f"Error in process_pdf_article: {str(e)}")
            return [TextContent(
                type="text", 
                text=f"Error processing PDF article: {str(e)}"
            )]
    
    elif name == "extract_pdf_text":
        try:
            file_path = arguments.get("file_path")
            
            if not file_path or not os.path.exists(file_path):
                return [TextContent(
                    type="text",
                    text="Error: File path not provided or file does not exist"
                )]
            
            result = extract_pdf_text(file_path)
            
            if result["success"]:
                response = f"""# PDF Text Extraction Results

## Document Information
- **File**: {file_path}
- **Title**: {result['metadata'].get('title', 'Not available')}
- **Author**: {result['metadata'].get('author', 'Not available')}
- **Pages**: {result['total_pages']}
- **Characters**: {result['total_chars']:,}

## Text Content Preview
{result['full_text'][:500]}{'...' if len(result['full_text']) > 500 else ''}
"""
            else:
                response = f"Error extracting PDF text: {result['error']}"
                
            return [TextContent(type="text", text=response)]
            
        except Exception as e:
            logger.error(f"Error in extract_pdf_text: {str(e)}")
            return [TextContent(
                type="text",
                text=f"Error extracting PDF text: {str(e)}"
            )]
    
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]

async def main():
    """Main server entry point."""
    # Initialize server options
    from mcp.server.models import ServerCapabilities
    
    options = InitializationOptions(
        server_name="academic-pdf-summarizer",
        server_version="0.1.0",
        capabilities=ServerCapabilities(
            tools={}
        )
    )
    
    logger.info("Starting Academic PDF Summarization MCP Server...")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            options
        )

if __name__ == "__main__":
    asyncio.run(main())