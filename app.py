#!/usr/bin/env python3
"""
Podcast Summarizer & Recommender - Main Application

This script provides a command-line interface to interact with the podcast 
summarizer and recommender system.
"""

import argparse
import logging
import os
import sys
import json
from typing import List, Dict, Any

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("podcast_tool.log")
    ]
)
logger = logging.getLogger(__name__)

# Import project modules
try:
    from src.data_collection.rss_feed import RSSFeedParser
    from src.data_collection.podcast_downloader import PodcastDownloader
except ImportError as e:
    logger.error(f"Failed to import project modules: {e}")
    logger.error("Make sure you're running from the project root directory")
    sys.exit(1)

def collect_podcasts(feed_urls: List[str], limit_per_podcast: int = 5) -> None:
    """
    Collect podcast data and download audio files.
    
    Args:
        feed_urls: List of RSS feed URLs
        limit_per_podcast: Maximum number of episodes to download per podcast
    """
    logger.info(f"Starting podcast collection from {len(feed_urls)} feeds")
    
    # Parse RSS feeds
    parser = RSSFeedParser()
    podcasts = parser.get_feeds_from_list(feed_urls)
    
    # Download podcast episodes
    downloader = PodcastDownloader()
    for podcast in podcasts:
        downloader.download_podcast(podcast, limit=limit_per_podcast)

def main():
    """Main entry point for the application."""
    
    # Define command-line arguments
    parser = argparse.ArgumentParser(
        description="Podcast Summarizer & Recommender",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Collect command
    collect_parser = subparsers.add_parser("collect", help="Collect podcast data")
    collect_parser.add_argument(
        "--feeds", "-f", 
        nargs="+", 
        help="List of RSS feed URLs"
    )
    collect_parser.add_argument(
        "--feed-file", 
        help="JSON file containing RSS feed URLs"
    )
    collect_parser.add_argument(
        "--limit", "-l", 
        type=int, 
        default=5, 
        help="Maximum number of episodes to download per podcast"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute command
    if args.command == "collect":
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
        
        if not feed_urls:
            logger.error("No feed URLs provided. Use --feeds or --feed-file")
            sys.exit(1)
        
        collect_podcasts(feed_urls, args.limit)
    else:
        # No command provided, show help
        parser.print_help()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        sys.exit(1) 