"""
Audio recording module for capturing microphone input.

This module was developed with significant assistance from AI tools (GitHub Copilot/Claude).
AI was used for code generation, documentation, debugging, and optimization.

Date: November 1, 2025
AI Assistant: GitHub Copilot (Claude Sonnet 4.5)
"""

from threading import Thread
from pathlib import Path
import sounddevice as sd
import soundfile as sf
import numpy as np
import whisper
import torch
import time

WHISPER_MODEL_SIZE = "medium"

class WhisperTranscriber:
    """
    Audio transcriber class using OpenAI's Whisper model.
    """

    def __init__(self, model_size: str = WHISPER_MODEL_SIZE):
        """Initialize the WhisperTranscriber with the specified model size."""
        
        self.model: whisper.Whisper = whisper.load_model(WHISPER_MODEL_SIZE)

    def transcribe(self, audio_path: Path) -> str:
        """
        Transcribe the audio file at the given path.

        Parameters
        ----------
        audio_path : Path
            The path to the audio file to transcribe.

        Returns
        -------
        str
            The transcribed text.
        """

        result = self.model.transcribe(str(audio_path))
        return result.get("text", "")

class Recorder:
    """
    Audio recorder class for capturing microphone input and saving to WAV files.
    """

    def __init__(self):
        """Initialize the Recorder with default settings."""

        self.deviceindex = None
        self.sample_rate = 16000
        self.channels = 1
        self.audio_data: list = []
        self.is_recording = False
        self.recordingThread: Thread = None
        self.stream = None

    def _record(self):
        """
        Internal method to handle audio recording in a background thread.
        
        Creates an audio input stream with a callback function that continuously
        captures audio data while recording is active. The stream remains open
        until recording is stopped.
        """

        def callback(indata, frames, time_info, status):
            if self.is_recording:
                self.audio_data.append(indata.copy())
        
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype='int16',
            device=self.deviceindex,
            callback=callback,
            blocksize=1024
        )
        
        self.stream.start()
        
        while self.is_recording:
            time.sleep(0.1)
        
        self.stream.stop()
        self.stream.close()

    def start_recording(self) -> bool:
        """
        Start recording audio from the microphone.
        
        Initializes audio capture in a background thread. If recording is already
        in progress, this method returns False without starting a new recording.
        
        Returns
        -------
        bool
            True if recording started successfully, False if already recording
            or if an error occurred.
        """

        if self.is_recording:
            return False
        
        try:
            self.audio_data = []
            self.is_recording = True
            self.recordingThread = Thread(target=self._record)
            self.recordingThread.start()
            
            time.sleep(0.1)
            return True
        except Exception as e:
            self.is_recording = False
            return False
        
    def stop_recording(self, output_path: Path) -> bool:
        """
        Stop recording and save the captured audio to a WAV file.
        
        Stops the audio capture, waits for the recording thread to finish,
        concatenates all audio chunks, and writes the result to the specified
        file path.
        
        Parameters
        ----------
        output_path : Path
            The file path where the recorded audio will be saved as a WAV file.
        
        Returns
        -------
        bool
            True if recording was stopped and saved successfully, False if
            not currently recording or if an error occurred during save.
        
        Notes
        -----
        The method will wait up to 2 seconds for the recording thread to finish.
        If no audio data was captured, the method returns False without creating
        a file.
        """

        if not self.is_recording:
            return False
            
        try:
            self.is_recording = False

            if self.recordingThread:
                self.recordingThread.join(timeout=2.0)  # Add timeout
            
            if not self.audio_data:
                return False
                
            audio_array = np.concatenate(self.audio_data, axis=0)
            sf.write(str(output_path), audio_array, self.sample_rate)
        
            return True
        except Exception as e:
            return False