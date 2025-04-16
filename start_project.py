#!/usr/bin/env python3
"""
Podcast Summarizer & Recommender - Startup Script

This script provides a simple interface to run different parts of the project.
"""

import os
import sys
import argparse
import logging
import subprocess

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("project.log")
    ]
)
logger = logging.getLogger(__name__)

def run_data_collection(limit=3):
    """Run the data collection module."""
    logger.info(f"Running data collection with limit={limit}")
    try:
        subprocess.run([
            sys.executable,
            "src/data_collection/scripts/collect_podcasts.py",
            "--limit", str(limit)
        ], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Data collection failed: {e}")
        return False
    return True

def run_web_interface(debug=True):
    """Run the web interface."""
    logger.info(f"Starting web interface (debug={debug})")
    try:
        cmd = [sys.executable, "src/web/run.py"]
        if debug:
            cmd.append("--debug")
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Web interface failed: {e}")
        return False
    return True

def setup_project():
    """Set up the project directories."""
    logger.info("Setting up project directories")
    try:
        # Import config to create directories
        import config
        logger.info("Project setup complete")
    except Exception as e:
        logger.error(f"Project setup failed: {e}")
        return False
    return True

def main():
    """Main entry point for the script."""
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Podcast Summarizer & Recommender Startup Script",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--action", "-a",
        choices=["setup", "collect", "web", "all"],
        default="all",
        help="Action to perform"
    )
    
    parser.add_argument(
        "--limit", "-l", 
        type=int, 
        default=3, 
        help="Maximum number of episodes to download per podcast"
    )
    
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        default=True,
        help="Run in debug mode"
    )
    
    args = parser.parse_args()
    
    # Execute actions
    if args.action == "setup" or args.action == "all":
        if not setup_project():
            sys.exit(1)
    
    if args.action == "collect" or args.action == "all":
        if not run_data_collection(args.limit):
            sys.exit(1)
    
    if args.action == "web" or args.action == "all":
        if not run_web_interface(args.debug):
            sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        sys.exit(1) 