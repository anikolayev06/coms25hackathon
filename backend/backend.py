from . import system_prompts
from typing import Optional
from . import conversation
from pathlib import Path
import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY_COMS25")

INTERVIEWER_ROLE, ASK_INTERVIEW_QUESTIONS, JOB_DESCRIPTION_CONTEXT, RESUME_CONTEXT, FEEDBACK_REQUEST = system_prompts.load_prompts()

chat = conversation.Conversation()

def prompt_gemini(input: str) -> Optional[str]:
    """
    Send a prompt to the Gemini model and return the text response if successful.

    Parameters
    ----------
    input : str
        The prompt text to send to Gemini.

    Returns
    -------
    Optional[str]
        The text response from Gemini on success, or None on failure.
    """

    return chat.prompt_gemini(input)

def submit_resume_pdf(pdf_path: Path) -> bool:
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

    return chat.submit_pdf(RESUME_CONTEXT, pdf_path)

def submit_job_description(input: str) -> bool:
    """
    Sumbit a job description for processing.

    Parameters
    ----------
    input : str
        The job description text to submit.

    Returns
    -------
    bool
        True if the submission was successful, False otherwise.
    """

    response = chat.prompt_gemini(f"{JOB_DESCRIPTION_CONTEXT}\n\nJob Description:\n{input}")
    return bool(response)

def ask_interview_question() -> Optional[str]:
    """
    Ask an interview question.

    Returns
    -------
    Optional[str]
        The question text if available, or None if not.
    """

    return prompt_gemini(ASK_INTERVIEW_QUESTIONS)

def answer_interview_question(input: str) -> Optional[str]:
    """
    Answer an interview question.

    Parameters
    ----------
    answer : str
        The answer text to the interview question.

    Returns
    -------
    Optional[str]
        The feedback text if available, or None if not.
    """

    return prompt_gemini(f"<candidate>{input}")

def get_interview_feedback() -> Optional[str]:
    """
    Get feedback on an interview.

    Returns
    -------
    Optional[str]
        The feedback text if available, or None if not.
    """

    return prompt_gemini(FEEDBACK_REQUEST)

def start_voice_recording() -> bool:
    """
    Start voice recording.

    Returns
    -------
    bool
        True if the recording started successfully, False otherwise.
    """

    pass

def stop_voice_recording() -> Optional[Path]:
    """
    Stop voice recording.

    Returns
    -------
    Optional[Path]
        The path to the recorded audio file if available, or None if not.
    """

    pass

def transcribe_audio(audio_path: Path) -> Optional[str]:
    """
    Transcribe audio from a given file path.

    Parameters
    ----------
    audio_path : Path
        The path to the audio file to transcribe.

    Returns
    -------
    Optional[str]
        The transcribed text if successful, or None on failure.
    """

    if not isinstance(audio_path, Path):
        audio_path = Path(audio_path)

    if not audio_path.exists() or not audio_path.is_file():
        return None
    
    transcription_chat = conversation.Conversation()

    myfile = transcription_chat.client.files.upload(fale=str(audio_path))

    response = transcription_chat.client.models.generate_content(
        model=conversation.GEMINI_MODEL,
        contents=["Generate a transcript of the speech.", myfile]
    )
    return getattr(response, "text", None)

def main():
    pass

if __name__ == "__main__":
    main()