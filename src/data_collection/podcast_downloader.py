"""
Podcast Audio Downloader

This module handles downloading podcast audio files from URLs.
"""

import os
import requests
from typing import Dict, Any, Optional, List
import logging
from urllib.parse import urlparse
from pathlib import Path
import json
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PodcastDownloader:
    """
    Downloads podcast audio files and saves metadata.
    """
    
    def __init__(self, 
                 audio_dir: str = "data/raw",
                 metadata_dir: str = "data/metadata",
                 max_retries: int = 3,
                 timeout: int = 30):
        """
        Initialize the podcast downloader.
        
        Args:
            audio_dir: Directory to save audio files
            metadata_dir: Directory to save metadata
            max_retries: Maximum number of download retry attempts
            timeout: Timeout for download requests in seconds
        """
        self.audio_dir = audio_dir
        self.metadata_dir = metadata_dir
        self.max_retries = max_retries
        self.timeout = timeout
        
        # Create directories if they don't exist
        os.makedirs(audio_dir, exist_ok=True)
        os.makedirs(metadata_dir, exist_ok=True)
    
    def download_episode(self, 
                       podcast_name: str,
                       episode_title: str, 
                       audio_url: str) -> Optional[str]:
        """
        Download a podcast episode audio file.
        
        Args:
            podcast_name: Name of the podcast
            episode_title: Title of the episode
            audio_url: URL to the audio file
            
        Returns:
            Path to the downloaded file or None if download failed
        """
        if not audio_url:
            logger.warning(f"No audio URL provided for {episode_title}")
            return None
        
        # Create sanitized filenames
        safe_podcast_name = "".join(c if c.isalnum() or c in [' ', '_', '-'] else '_' for c in podcast_name).strip()
        safe_episode_title = "".join(c if c.isalnum() or c in [' ', '_', '-'] else '_' for c in episode_title).strip()
        
        # Create podcast-specific directory
        podcast_dir = os.path.join(self.audio_dir, safe_podcast_name)
        os.makedirs(podcast_dir, exist_ok=True)
        
        # Determine file extension from URL
        parsed_url = urlparse(audio_url)
        path = parsed_url.path
        extension = os.path.splitext(path)[1]
        if not extension or extension.lower() not in ['.mp3', '.m4a', '.wav', '.ogg']:
            extension = '.mp3'  # Default to mp3 if extension is unknown
            
        # Create file path
        file_path = os.path.join(podcast_dir, f"{safe_episode_title}{extension}")
        
        # Skip if file already exists
        if os.path.exists(file_path):
            logger.info(f"File already exists: {file_path}")
            return file_path
        
        # Download the file
        logger.info(f"Downloading {episode_title} from {audio_url}")
        for attempt in range(self.max_retries):
            try:
                response = requests.get(audio_url, stream=True, timeout=self.timeout)
                response.raise_for_status()
                
                # Save file
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                logger.info(f"Successfully downloaded: {file_path}")
                return file_path
            except requests.exceptions.RequestException as e:
                logger.error(f"Download error (attempt {attempt+1}/{self.max_retries}): {e}")
                time.sleep(2 ** attempt)  # Exponential backoff
        
        logger.error(f"Failed to download {episode_title} after {self.max_retries} attempts")
        return None
    
    def download_podcast(self, podcast_data: Dict[str, Any], limit: int = None) -> List[str]:
        """
        Download all episodes for a podcast.
        
        Args:
            podcast_data: Dictionary containing podcast metadata and episodes
            limit: Maximum number of episodes to download (None for all)
            
        Returns:
            List of paths to downloaded audio files
        """
        podcast_name = podcast_data.get("title", "Unknown")
        episodes = podcast_data.get("episodes", [])
        
        if limit:
            episodes = episodes[:limit]
        
        # Save podcast metadata
        metadata_path = os.path.join(self.metadata_dir, f"{podcast_name.replace(' ', '_')}.json")
        with open(metadata_path, 'w') as f:
            json.dump(podcast_data, f, indent=2)
            
        # Download episodes
        downloaded_files = []
        for episode in episodes:
            audio_url = episode.get("audio_url")
            episode_title = episode.get("title", "Unknown")
            
            file_path = self.download_episode(podcast_name, episode_title, audio_url)
            if file_path:
                downloaded_files.append(file_path)
        
        logger.info(f"Downloaded {len(downloaded_files)} episodes for {podcast_name}")
        return downloaded_files 