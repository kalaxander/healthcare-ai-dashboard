from faster_whisper import WhisperModel
import os

# Global variable to cache the model
_whisper_model = None

def setup_whisper():
    """Initializes the Whisper model and caches it."""
    global _whisper_model
    
    if _whisper_model is not None:
        return _whisper_model
        
    print("Loading local Whisper 'base' model... (First run may take a moment to download)")
    
    # FIX: Force device="cpu" and compute_type="int8" to avoid missing NVIDIA CUDA drivers
    _whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
    
    return _whisper_model

def transcribe_audio(audio_path):
    """
    Takes a path to an audio file (.wav), runs it through Whisper, 
    and returns the transcribed text.
    """
    model = setup_whisper()
    
    # Transcribe the audio file
    segments, info = model.transcribe(audio_path, beam_size=5)
    
    # Combine the segments into a single string
    transcription = ""
    for segment in segments:
        transcription += segment.text + " "
        
    return transcription.strip()