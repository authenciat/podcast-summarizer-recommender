"""
Flask Web Application for Podcast Summarizer & Recommender

This module implements a web interface for browsing podcast summaries
and receiving personalized recommendations.
"""

from flask import Flask, render_template, request, jsonify
import os
import sys
import json
import logging

# Add project root to path to allow importing from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import project modules
import config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("web_app.log")
    ]
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

@app.route('/')
def home():
    """Home page route."""
    return render_template('index.html', title="Podcast Summarizer & Recommender")

@app.route('/podcasts')
def podcasts():
    """Podcasts page route."""
    # Load podcast metadata
    podcasts_data = []
    try:
        metadata_files = [f for f in os.listdir(config.METADATA_DIR) if f.endswith('.json')]
        for file in metadata_files:
            with open(os.path.join(config.METADATA_DIR, file), 'r') as f:
                podcast = json.load(f)
                podcasts_data.append({
                    'title': podcast.get('title', 'Unknown'),
                    'author': podcast.get('author', 'Unknown'),
                    'description': podcast.get('description', ''),
                    'image': podcast.get('image', ''),
                    'episode_count': len(podcast.get('episodes', []))
                })
    except Exception as e:
        logger.error(f"Error loading podcast metadata: {e}")
    
    return render_template('podcasts.html', 
                         title="Browse Podcasts",
                         podcasts=podcasts_data)

@app.route('/podcast/<podcast_name>')
def podcast_detail(podcast_name):
    """Podcast detail page route."""
    # Load podcast metadata
    podcast_data = None
    
    # Try to find the podcast file by name
    try:
        # First try direct match
        file_path = os.path.join(config.METADATA_DIR, f"{podcast_name}.json")
        if not os.path.exists(file_path):
            # If not found, try searching through all metadata files
            logger.info(f"Podcast file not found directly: {file_path}, searching through all files")
            for filename in os.listdir(config.METADATA_DIR):
                if filename.endswith('.json'):
                    with open(os.path.join(config.METADATA_DIR, filename), 'r') as f:
                        data = json.load(f)
                        # Check if this is the podcast we're looking for
                        podcast_title = data.get('title', '')
                        if podcast_title and (podcast_name == podcast_title.replace(' ', '_')):
                            file_path = os.path.join(config.METADATA_DIR, filename)
                            logger.info(f"Found matching podcast: {file_path}")
                            break
        
        # Load the podcast data
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                podcast_data = json.load(f)
        else:
            logger.error(f"No matching podcast file found for: {podcast_name}")
            return render_template('error.html', 
                                 title="Podcast Not Found",
                                 message=f"Podcast '{podcast_name.replace('_', ' ')}' not found")
    except Exception as e:
        logger.error(f"Error loading podcast metadata for {podcast_name}: {e}")
        return render_template('error.html', 
                             title="Podcast Not Found",
                             message=f"Podcast '{podcast_name.replace('_', ' ')}' not found")
    
    return render_template('podcast_detail.html', 
                         title=podcast_data.get('title', 'Unknown'),
                         podcast=podcast_data)

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """API endpoint for podcast recommendations."""
    # Get request data
    data = request.get_json() or {}
    podcast_id = data.get('podcast_id')
    user_id = data.get('user_id')
    
    # This is a placeholder for the actual recommendation logic
    # In a real implementation, this would use the recommendation module
    
    recommendations = [
        {'title': 'Recommended Podcast 1', 'similarity': 0.95},
        {'title': 'Recommended Podcast 2', 'similarity': 0.87},
        {'title': 'Recommended Podcast 3', 'similarity': 0.82}
    ]
    
    return jsonify({
        'recommendations': recommendations,
        'status': 'success'
    })

def run_app(host=None, port=None, debug=None):
    """Run the Flask application."""
    host = host or config.FLASK_HOST
    port = port or config.FLASK_PORT
    debug = debug if debug is not None else config.FLASK_DEBUG
    
    logger.info(f"Starting Flask app on {host}:{port} (debug={debug})")
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    run_app() 