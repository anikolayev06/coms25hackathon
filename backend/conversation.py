from google.genai.types import GenerateContentResponse
from google.genai import types
from google import genai
from typing import Optional
from google import genai
from pathlib import Path
import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY_COMS25")
GEMINI_MODEL = "gemini-2.5-flash"

class Conversation:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.chat = self.client.chats.create(model=GEMINI_MODEL)

    def prompt_gemini(self, input: str) -> Optional[str]:
        """
        Send a prompt to the Gemini model and return the text response if successful.

        Parameters
        ----------
        input : str
            The prompt text to send to Gemini.

        Raises
        ------
        ValueError
            If the GEMINI_API_KEY is not set.
        ConnectionError
            If the connection to the Gemini API fails.

        Returns
        -------
        Optional[str]
            The text response from Gemini on success, or None on failure.
        """

        response: GenerateContentResponse = self.chat.send_message(input)
        if not response: return None
        return response.text

    def submit_pdf(self, prompt: str, pdf_path: Path) -> bool:
        """
        Submit a resume PDF for processing.

        Parameters
        ----------
        pdf_path : Path
            The path to the PDF file to submit.

        Returns
        -------
        bool
            True if the submission was successful, False otherwise.
        """

        if not pdf_path.exists() or not pdf_path.is_file():
            return False
    
        if pdf_path.suffix.lower() != ".pdf":
            return False

        response = self.client.models.generate_content(
             model=GEMINI_MODEL,
             contents=[
                 types.Part.from_bytes(
                     data=pdf_path.read_bytes(),
                     mime_type="application/pdf",
                ),
                 prompt
            ],
        )
        
        return bool(getattr(response, "text", None))