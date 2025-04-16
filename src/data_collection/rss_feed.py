"""
RSS Feed Parser for Podcast Data Collection

This module handles retrieving podcast episode information from RSS feeds.
"""

import os
import feedparser
import requests
from typing import List, Dict, Any, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RSSFeedParser:
    """
    Parser for RSS feeds to extract podcast metadata and episode information.
    """
    
    def __init__(self, cache_dir: str = "data/metadata"):
        """
        Initialize the RSS feed parser.
        
        Args:
            cache_dir: Directory to cache RSS feed data
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def parse_feed(self, feed_url: str) -> Dict[str, Any]:
        """
        Parse a podcast RSS feed and extract relevant information.
        
        Args:
            feed_url: URL of the RSS feed
            
        Returns:
            Dictionary containing podcast metadata and episodes
        """
        logger.info(f"Parsing RSS feed: {feed_url}")
        feed = feedparser.parse(feed_url)
        
        # Extract podcast metadata
        podcast_data = {
            "title": feed.feed.get("title", "Unknown"),
            "description": feed.feed.get("description", ""),
            "link": feed.feed.get("link", ""),
            "image": feed.feed.get("image", {}).get("href", ""),
            "language": feed.feed.get("language", "en"),
            "author": feed.feed.get("author", "Unknown"),
            "episodes": []
        }
        
        # Extract episode data
        for entry in feed.entries:
            episode = {
                "title": entry.get("title", "Unknown"),
                "description": entry.get("description", ""),
                "published": entry.get("published", ""),
                "duration": entry.get("itunes_duration", ""),
                "link": entry.get("link", ""),
                "audio_url": None
            }
            
            # Extract audio URL
            if "enclosures" in entry and len(entry.enclosures) > 0:
                for enclosure in entry.enclosures:
                    if enclosure.get("type", "").startswith("audio/"):
                        episode["audio_url"] = enclosure.get("href", None)
                        break
            
            podcast_data["episodes"].append(episode)
        
        logger.info(f"Found {len(podcast_data['episodes'])} episodes for {podcast_data['title']}")
        return podcast_data
    
    def get_feeds_from_list(self, feed_urls: List[str]) -> List[Dict[str, Any]]:
        """
        Parse multiple podcast RSS feeds.
        
        Args:
            feed_urls: List of RSS feed URLs
            
        Returns:
            List of dictionaries containing podcast metadata and episodes
        """
        podcasts = []
        for url in feed_urls:
            try:
                podcast_data = self.parse_feed(url)
                podcasts.append(podcast_data)
            except Exception as e:
                logger.error(f"Error parsing feed {url}: {e}")
        
        return podcasts 