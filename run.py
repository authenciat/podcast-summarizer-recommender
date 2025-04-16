#!/usr/bin/env python3
"""
Podcast Summarizer & Recommender - Main Run Script

This script provides a simple CLI to run different components of the project.
"""

import argparse
import subprocess
import sys
import os

def main():
    """Main entry point for the script."""
    
    # Create argument parser
    parser = argparse.ArgumentParser(
        description="Podcast Summarizer & Recommender",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Add subparsers
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
        default=3, 
        help="Maximum number of episodes to download per podcast"
    )
    
    # Web command
    web_parser = subparsers.add_parser("web", help="Run web interface")
    web_parser.add_argument(
        "--debug", "-d",
        action="store_true",
        default=True,
        help="Run in debug mode"
    )
    web_parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind to"
    )
    web_parser.add_argument(
        "--port", "-p",
        type=int,
        default=5000,
        help="Port to listen on"
    )
    
    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Set up project")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Run tests")
    test_parser.add_argument(
        "--test-file", "-t",
        help="Specific test file to run"
    )
    
    # All command - runs all components in sequence
    all_parser = subparsers.add_parser("all", help="Run all components")
    all_parser.add_argument(
        "--limit", "-l", 
        type=int, 
        default=3, 
        help="Maximum number of episodes to download per podcast"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    if args.command == "collect":
        # Run collect command
        collect_cmd = ["python", "app.py", "collect"]
        
        if args.feeds:
            collect_cmd.extend(["--feeds"] + args.feeds)
        
        if args.feed_file:
            collect_cmd.extend(["--feed-file", args.feed_file])
        
        collect_cmd.extend(["--limit", str(args.limit)])
        
        subprocess.run(collect_cmd)
        
    elif args.command == "web":
        # Run web interface
        web_cmd = ["python", "src/web/run.py"]
        
        if args.debug:
            web_cmd.append("--debug")
        
        web_cmd.extend(["--host", args.host, "--port", str(args.port)])
        
        subprocess.run(web_cmd)
        
    elif args.command == "setup":
        # Run project setup
        print("Setting up project directories...")
        # Import config to create directories
        import config
        print("Project setup complete!")
        
    elif args.command == "test":
        # Run tests
        if args.test_file:
            test_cmd = ["python", "-m", "unittest", args.test_file]
        else:
            test_cmd = ["python", "-m", "unittest", "discover", "tests"]
        
        subprocess.run(test_cmd)
        
    elif args.command == "all":
        # Run all components
        
        # Setup
        print("Setting up project directories...")
        import config
        print("Project setup complete!")
        
        # Collect data
        print("\nCollecting podcast data...")
        collect_cmd = ["python", "app.py", "collect", "--limit", str(args.limit)]
        subprocess.run(collect_cmd)
        
        # Run web interface
        print("\nStarting web interface...")
        web_cmd = ["python", "src/web/run.py"]
        subprocess.run(web_cmd)
        
    else:
        # No command provided, show help
        parser.print_help()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1) 