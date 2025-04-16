"""
Audio Preprocessor for Speech-to-Text

This module handles preprocessing of audio files for the custom transcription system.
"""

import os
import numpy as np
import librosa
import logging
from typing import Tuple, Optional, Dict, Any
import soundfile as sf
from pydub import AudioSegment

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioPreprocessor:
    """
    Preprocesses audio files for speech recognition.
    """
    
    def __init__(self, 
                 target_sr: int = 16000,
                 max_duration: float = 30.0,
                 min_duration: float = 1.0,
                 temp_dir: str = "data/temp"):
        """
        Initialize the audio preprocessor.
        
        Args:
            target_sr: Target sample rate in Hz
            max_duration: Maximum duration of audio segments in seconds
            min_duration: Minimum duration of audio segments in seconds
            temp_dir: Directory for temporary files
        """
        self.target_sr = target_sr
        self.max_duration = max_duration
        self.min_duration = min_duration
        self.temp_dir = temp_dir
        
        os.makedirs(temp_dir, exist_ok=True)
    
    def load_audio(self, file_path: str) -> Tuple[np.ndarray, int]:
        """
        Load an audio file and convert to the target sample rate.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Tuple of (audio_array, sample_rate)
        """
        logger.info(f"Loading audio from {file_path}")
        try:
            audio, sr = librosa.load(file_path, sr=self.target_sr, mono=True)
            return audio, sr
        except Exception as e:
            logger.error(f"Error loading audio file {file_path}: {e}")
            
            # Fallback to pydub for problematic files
            logger.info("Attempting to load file with pydub...")
            try:
                # Convert file using pydub first
                audio_segment = AudioSegment.from_file(file_path)
                audio_segment = audio_segment.set_channels(1)  # Convert to mono
                
                # Export to temporary WAV file
                temp_path = os.path.join(self.temp_dir, "temp_conversion.wav")
                audio_segment.export(temp_path, format="wav")
                
                # Load with librosa
                audio, sr = librosa.load(temp_path, sr=self.target_sr, mono=True)
                return audio, sr
            except Exception as fallback_error:
                logger.error(f"Fallback loading failed: {fallback_error}")
                raise RuntimeError(f"Could not load audio file: {file_path}")
    
    def segment_audio(self, audio: np.ndarray, sr: int, 
                      silence_threshold: float = 0.03, 
                      min_silence_duration: float = 0.5) -> list:
        """
        Segment audio based on silence detection.
        
        Args:
            audio: Audio array
            sr: Sample rate
            silence_threshold: Threshold for silence detection (0-1)
            min_silence_duration: Minimum silence duration in seconds
            
        Returns:
            List of audio segments as numpy arrays
        """
        # Convert parameters to samples
        min_silence_samples = int(min_silence_duration * sr)
        
        # Calculate energy
        energy = librosa.feature.rms(y=audio)[0]
        silence_mask = energy < silence_threshold
        
        # Find silence regions
        silence_regions = []
        in_silence = False
        current_start = 0
        
        for i, is_silence in enumerate(silence_mask):
            if is_silence and not in_silence:
                in_silence = True
                current_start = i
            elif not is_silence and in_silence:
                in_silence = False
                duration = i - current_start
                if duration >= min_silence_samples:
                    silence_regions.append((current_start, i))
        
        # Add the last region if needed
        if in_silence:
            duration = len(silence_mask) - current_start
            if duration >= min_silence_samples:
                silence_regions.append((current_start, len(silence_mask)))
        
        # Create segments based on silence regions
        segments = []
        prev_end = 0
        
        for start, end in silence_regions:
            # Convert frame indices to sample indices
            start_sample = librosa.frames_to_samples(start)
            end_sample = librosa.frames_to_samples(end)
            
            if start_sample > prev_end:
                segment = audio[prev_end:start_sample]
                segment_duration = len(segment) / sr
                
                if segment_duration >= self.min_duration:
                    segments.append(segment)
            
            prev_end = end_sample
        
        # Add the final segment if needed
        if prev_end < len(audio):
            segment = audio[prev_end:]
            segment_duration = len(segment) / sr
            
            if segment_duration >= self.min_duration:
                segments.append(segment)
        
        logger.info(f"Segmented audio into {len(segments)} parts")
        return segments
    
    def process_audio(self, file_path: str) -> Dict[str, Any]:
        """
        Process an audio file for transcription.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Dictionary with processed audio data
        """
        audio, sr = self.load_audio(file_path)
        
        # Calculate duration
        duration = librosa.get_duration(y=audio, sr=sr)
        logger.info(f"Audio duration: {duration:.2f} seconds")
        
        # Calculate features needed for transcription
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
        
        # Segment audio if longer than max duration
        segments = []
        if duration > self.max_duration:
            segments = self.segment_audio(audio, sr)
        else:
            segments = [audio]
        
        return {
            "file_path": file_path,
            "sample_rate": sr,
            "duration": duration,
            "mfccs": mfccs,
            "segments": segments,
            "num_segments": len(segments)
        } 