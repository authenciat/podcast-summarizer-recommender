"""
Configuration Settings for Podcast Summarizer & Recommender

This file contains configuration parameters for the project.
"""

import os
from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent.absolute()
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")

# Data subdirectories
RAW_AUDIO_DIR = os.path.join(DATA_DIR, "raw")
TRANSCRIPTIONS_DIR = os.path.join(DATA_DIR, "transcriptions")
SUMMARIES_DIR = os.path.join(DATA_DIR, "summaries")
METADATA_DIR = os.path.join(DATA_DIR, "metadata")
TEMP_DIR = os.path.join(DATA_DIR, "temp")

# Model subdirectories
TRANSCRIPTION_MODEL_DIR = os.path.join(MODELS_DIR, "transcription")
SUMMARIZATION_MODEL_DIR = os.path.join(MODELS_DIR, "summarization")
TOPIC_MODEL_DIR = os.path.join(MODELS_DIR, "topic")

# Audio processing settings
SAMPLE_RATE = 16000
MAX_AUDIO_DURATION = 30.0  # in seconds
MIN_AUDIO_DURATION = 1.0  # in seconds

# Transcription settings
PHONEME_CLASSES = 40  # Number of phoneme classes to recognize
TRANSCRIPTION_BATCH_SIZE = 16

# Summarization settings
MAX_INPUT_LENGTH = 1024  # Maximum input length for summarization
MAX_SUMMARY_LENGTH = 250  # Maximum summary length in tokens
MIN_SUMMARY_LENGTH = 50  # Minimum summary length in tokens
T5_MODEL_NAME = "t5-base"  # Base model for summarization

# Topic modeling settings
NUM_TOPICS = 20  # Number of topics to extract
TOP_N_WORDS = 10  # Number of words to show per topic
BERTOPIC_LANGUAGE = "english"

# Web interface settings
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = True

# API settings
PODCAST_INDEX_API_KEY = os.environ.get("PODCAST_INDEX_API_KEY", "")
PODCAST_INDEX_API_SECRET = os.environ.get("PODCAST_INDEX_API_SECRET", "")

# Create directories if they don't exist
for directory in [
    DATA_DIR, 
    RAW_AUDIO_DIR, 
    TRANSCRIPTIONS_DIR, 
    SUMMARIES_DIR, 
    METADATA_DIR,
    TEMP_DIR,
    MODELS_DIR,
    TRANSCRIPTION_MODEL_DIR,
    SUMMARIZATION_MODEL_DIR,
    TOPIC_MODEL_DIR
]:
    os.makedirs(directory, exist_ok=True) 