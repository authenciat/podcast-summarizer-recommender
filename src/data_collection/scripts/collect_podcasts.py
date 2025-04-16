#!/usr/bin/env python3
"""
Podcast Collection Script

This script demonstrates how to collect podcast data from RSS feeds.
"""

import os
import sys
import json
import logging
import argparse
from typing import List

# Add project root to path to allow importing from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Import project modules
from src.data_collection.rss_feed import RSSFeedParser
from src.data_collection.podcast_downloader import PodcastDownloader
import config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("podcast_collection.log")
    ]
)
logger = logging.getLogger(__name__)

def collect_podcasts(feed_urls: List[str], limit_per_podcast: int = 3) -> None:
    """
    Collect podcast data from RSS feeds.
    
    Args:
        feed_urls: List of RSS feed URLs
        limit_per_podcast: Maximum number of episodes to download per podcast
    """
    logger.info(f"Starting podcast collection from {len(feed_urls)} feeds")
    
    # Parse RSS feeds
    parser = RSSFeedParser(cache_dir=config.METADATA_DIR)
    podcasts = parser.get_feeds_from_list(feed_urls)
    
    # Download podcast episodes
    downloader = PodcastDownloader(
        audio_dir=config.RAW_AUDIO_DIR,
        metadata_dir=config.METADATA_DIR
    )
    
    for podcast in podcasts:
        downloaded_files = downloader.download_podcast(podcast, limit=limit_per_podcast)
        logger.info(f"Downloaded {len(downloaded_files)} episodes for {podcast['title']}")

def main():
    """Main entry point for the script."""
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Collect podcast data from RSS feeds",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--feeds", "-f", 
        nargs="+", 
        help="List of RSS feed URLs"
    )
    
    parser.add_argument(
        "--feed-file", 
        help="JSON file containing RSS feed URLs"
    )
    
    parser.add_argument(
        "--limit", "-l", 
        type=int, 
        default=3, 
        help="Maximum number of episodes to download per podcast"
    )
    
    args = parser.parse_args()
    
    # Get feed URLs
    feed_urls = []
    
    # Get feed URLs from command line arguments
    if args.feeds:
        feed_urls.extend(args.feeds)
    
    # Get feed URLs from JSON file
    if args.feed_file:
        try:
            with open(args.feed_file, 'r') as f:
                feed_data = json.load(f)
                if isinstance(feed_data, list):
                    feed_urls.extend(feed_data)
                elif isinstance(feed_data, dict) and "feeds" in feed_data:
                    feed_urls.extend(feed_data["feeds"])
        except Exception as e:
            logger.error(f"Failed to read feed file: {e}")
    
    # Use default feed file if no feeds provided
    if not feed_urls:
        default_feed_file = os.path.join(os.path.dirname(__file__), '../../../feeds.json')
        if os.path.exists(default_feed_file):
            logger.info(f"Using default feed file: {default_feed_file}")
            try:
                with open(default_feed_file, 'r') as f:
                    feed_data = json.load(f)
                    if isinstance(feed_data, list):
                        feed_urls.extend(feed_data)
                    elif isinstance(feed_data, dict) and "feeds" in feed_data:
                        feed_urls.extend(feed_data["feeds"])
            except Exception as e:
                logger.error(f"Failed to read default feed file: {e}")
    
    if not feed_urls:
        logger.error("No feed URLs provided. Use --feeds or --feed-file")
        sys.exit(1)
    
    # Collect podcasts
    collect_podcasts(feed_urls, args.limit)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        sys.exit(1) 