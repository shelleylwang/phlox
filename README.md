# Academic PDF Summarization MCP Server

A Model Context Protocol (MCP) server for processing and summarizing academic PDF articles. This is the Hour 1 MVP implementation focusing on basic PDF text extraction and MCP server functionality.

## Quick Start

### 1. Install Dependencies
```bash
python setup.py
```

### 2. Run the MCP Server
```bash
python mcp_server.py
```

### 3. Test with a PDF
The server provides two MCP tools:
- `process_pdf_article`: Process a base64-encoded PDF
- `extract_pdf_text`: Extract text from a local PDF file (for testing)

## Features (Hour 1 Implementation)

✅ **Core Infrastructure**
- Working MCP server with stdio communication
- Basic project structure and dependency management
- Error handling for common failure cases

✅ **PDF Processing**
- Text extraction from academic PDFs using PyMuPDF
- Metadata extraction (title, author, page count)
- Support for multi-page documents
- Base64 file handling for web integration

✅ **MCP Integration**
- Two working MCP tools for different use cases
- Proper tool registration and argument handling
- Structured text output with metadata

## Usage Examples

### With AI Assistant (Claude, ChatGPT, etc.)
Once the MCP server is running, you can use it with compatible AI assistants:

```
"Please process this PDF article and extract the text content."
[Upload PDF file]
```

### Direct Testing
You can test the server directly with a local PDF:

```python
# The server will respond to MCP tool calls
{
    "tool": "extract_pdf_text",  
    "arguments": {
        "file_path": "/path/to/your/academic_paper.pdf"
    }
}
```

## Output Format

The server returns structured information including:
- Document metadata (title, author, page count)
- Full extracted text content
- Character count and processing statistics
- Error handling messages when issues occur

## Technical Details

- **Framework**: Python MCP SDK
- **PDF Processing**: PyMuPDF (fitz)
- **Communication**: Standard I/O (stdio)
- **Error Handling**: Comprehensive exception handling
- **File Handling**: Temporary file management for base64 uploads

## Next Steps (Hours 2-3)

- Add LLM integration for summarization
- Implement document structure detection
- Create academic-focused summary generation
- Add multiple output formats
- Enhanced error handling and validation

## Requirements

- Python 3.8+
- MCP framework (`pip install mcp>=0.9.0`)
- PyMuPDF (`pip install PyMuPDF>=1.23.0`)

## Troubleshooting

### Common Issues
1. **Import Errors**: Run `python setup.py` to install dependencies
2. **PDF Processing Errors**: Ensure PDF is not password-protected or corrupted
3. **MCP Connection Issues**: Check that the server is running and accessible

### Logging
The server includes comprehensive logging. Check console output for detailed error messages and processing information.

## Development

This is a minimal viable product (MVP) designed to be completed in 1 hour. The code is structured for easy extension and enhancement in subsequent development phases.