"""
Text Preprocessor for Summarization

This module handles preprocessing of podcast transcriptions for the summarization model.
"""

import re
import nltk
import logging
from typing import List, Dict, Any, Optional
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download NLTK resources if not already present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class TextPreprocessor:
    """
    Preprocesses text transcriptions for summarization.
    """
    
    def __init__(self, 
                max_input_length: int = 1024,
                min_sentence_length: int = 5,
                language: str = "english"):
        """
        Initialize the text preprocessor.
        
        Args:
            max_input_length: Maximum input length in tokens
            min_sentence_length: Minimum sentence length in words
            language: Language for stopwords
        """
        self.max_input_length = max_input_length
        self.min_sentence_length = min_sentence_length
        self.language = language
        self.stopwords = set(stopwords.words(language))
    
    def clean_text(self, text: str) -> str:
        """
        Clean text by removing unnecessary characters and formatting.
        
        Args:
            text: Input text
            
        Returns:
            Cleaned text
        """
        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text)
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S*@\S*\s?', '', text)
        
        # Remove special characters except punctuation
        text = re.sub(r'[^\w\s.,!?;:\-\'"]', '', text)
        
        # Fix spacing around punctuation
        text = re.sub(r'\s([.,!?;:])', r'\1', text)
        
        return text.strip()
    
    def split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences.
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        sentences = sent_tokenize(text)
        
        # Filter out short sentences
        filtered_sentences = []
        for sentence in sentences:
            words = word_tokenize(sentence)
            if len(words) >= self.min_sentence_length:
                filtered_sentences.append(sentence)
        
        return filtered_sentences
    
    def filter_filler_words(self, text: str) -> str:
        """
        Remove common filler words and phrases from podcast transcripts.
        
        Args:
            text: Input text
            
        Returns:
            Filtered text
        """
        filler_phrases = [
            r'\bum\b', r'\buh\b', r'\blike\b', r'\byou know\b', 
            r'\bI mean\b', r'\bsort of\b', r'\bkind of\b', 
            r'\bbasically\b', r'\bliterally\b', r'\bactually\b'
        ]
        
        for phrase in filler_phrases:
            text = re.sub(phrase, '', text, flags=re.IGNORECASE)
        
        # Clean up extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def truncate_to_max_length(self, tokens: List[str]) -> List[str]:
        """
        Truncate tokens to max input length.
        
        Args:
            tokens: List of tokens
            
        Returns:
            Truncated list of tokens
        """
        if len(tokens) <= self.max_input_length:
            return tokens
        
        return tokens[:self.max_input_length]
    
    def preprocess(self, transcript: str) -> Dict[str, Any]:
        """
        Preprocess a transcript for summarization.
        
        Args:
            transcript: Transcript text
            
        Returns:
            Dictionary with preprocessed text data
        """
        # Clean text
        cleaned_text = self.clean_text(transcript)
        
        # Filter filler words
        filtered_text = self.filter_filler_words(cleaned_text)
        
        # Split into sentences
        sentences = self.split_into_sentences(filtered_text)
        
        # Tokenize
        tokens = word_tokenize(filtered_text)
        
        # Truncate if needed
        truncated_tokens = self.truncate_to_max_length(tokens)
        truncated_text = ' '.join(truncated_tokens)
        
        result = {
            "original_length": len(transcript),
            "cleaned_text": filtered_text,
            "sentences": sentences,
            "num_sentences": len(sentences),
            "tokens": truncated_tokens,
            "truncated_text": truncated_text,
            "truncated_length": len(truncated_tokens)
        }
        
        logger.info(f"Preprocessed text: {result['original_length']} chars -> {result['truncated_length']} tokens")
        return result 