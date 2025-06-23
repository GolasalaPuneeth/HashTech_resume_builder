CHUNK_SIZE = 1024
from weasyprint import HTML
import io
from typing import Generator, AsyncGenerator

async def generate_pdf_bytes_chunked(html_content: str) -> AsyncGenerator[bytes, None]:
    """
    Generates a PDF from HTML content using WeasyPrint and yields it in chunks.

    Args:
        html_content (str): The HTML string to convert to PDF.

    Yields:
        bytes: Chunks of the generated PDF binary data.
    """
    # Create an in-memory binary stream to hold the complete PDF data temporarily.
    # WeasyPrint generates the entire PDF first, so we capture it in BytesIO.
    pdf_bytes_io = io.BytesIO()

    # Generate the PDF from the HTML content and write it into the BytesIO object.
    # This is the CPU-intensive part where WeasyPrint processes the HTML.
    HTML(string=html_content).write_pdf(pdf_bytes_io)

    # Move the stream's cursor to the beginning (0) so we can read from it.
    pdf_bytes_io.seek(0)

    # Read the PDF content in chunks and yield each chunk.
    # This loop ensures that the data is streamed piece by piece rather than all at once.
    while True:
        chunk = pdf_bytes_io.read(CHUNK_SIZE)
        if not chunk:
            # If no more chunks are read, we've reached the end of the PDF data.
            break
        yield chunk
    
    # The BytesIO object will be automatically garbage collected after the function scope ends.