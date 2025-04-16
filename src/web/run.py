#!/usr/bin/env python3
"""
Run the Podcast Summarizer & Recommender Web Application

This script starts the Flask web server for the project.
"""

import os
import sys
import argparse

# Add project root to path to allow importing from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import app module
from src.web.app import run_app
import config

def main():
    """Main entry point for the script."""
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Run the Podcast Summarizer & Recommender Web Application",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--host", 
        default=config.FLASK_HOST, 
        help="Host address to bind the server to"
    )
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=config.FLASK_PORT, 
        help="Port to run the server on"
    )
    
    parser.add_argument(
        "--debug", 
        action="store_true", 
        default=config.FLASK_DEBUG, 
        help="Run in debug mode"
    )
    
    args = parser.parse_args()
    
    # Run the application
    run_app(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main() 