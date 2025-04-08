!pip install feedparser pydub transformers torch librosa

import os
import feedparser
import requests
from pydub import AudioSegment
from transformers import T5Tokenizer, T5ForConditionalGeneration

def download_audio_from_rss(feed_url, save_dir="podcast_data", limit=3):
    os.makedirs(save_dir, exist_ok=True)
    feed = feedparser.parse(feed_url)
    
    for entry in feed.entries[:limit]:
        try:
            title = entry.title.replace(" ", "_").replace("/", "_")
            audio_url = entry.enclosures[0]['href']
            file_path = os.path.join(save_dir, f"{title}.mp3")
            print(f"Downloading: {title}")
            audio_data = requests.get(audio_url)
            with open(file_path, 'wb') as f:
                f.write(audio_data.content)
        except Exception as e:
            print(f"Error downloading {entry.title}: {e}")
