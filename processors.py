import PyPDF2

class DocumentProcessor:
    def __init__(self, uploaded_file):
        """Initializes with the Streamlit file object."""
        self.uploaded_file = uploaded_file

    def extract_text(self) -> str:
        """Extracts text from the PDF safely."""
        try:
            reader = PyPDF2.PdfReader(self.uploaded_file)
            extracted_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
            
            if not extracted_text.strip():
                raise ValueError("The PDF appears to be empty or an image scan.")
            return extracted_text
        except Exception as e:
            return f"Error: {str(e)}"