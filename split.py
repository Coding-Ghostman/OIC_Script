import PyPDF2
import base64
import io


def split_pdf(pdf_content: bytes) -> str:
    encoded_string = ""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
        pdf_writer = PyPDF2.PdfWriter()

        for page_num in range(2):  # First two pages
            pdf_writer.add_page(pdf_reader.pages[page_num])

        temp_pdf_bytes = io.BytesIO()
        pdf_writer.write(temp_pdf_bytes)
        temp_pdf_bytes.seek(0)

        encoded_string = base64.b64encode(temp_pdf_bytes.read()).decode("utf-8")
    except Exception as e:
        print(f"Error in split_pdf: {e}")
    finally:
        return encoded_string
