"""
Tests for the Data Collection Module

This module contains unit tests for the data collection components.
"""

import os
import sys
import unittest
import json
import tempfile
from unittest.mock import patch, MagicMock

# Add project root to path to allow importing from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import project modules
from src.data_collection.rss_feed import RSSFeedParser
from src.data_collection.podcast_downloader import PodcastDownloader

class TestRSSFeedParser(unittest.TestCase):
    """Tests for the RSSFeedParser class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.parser = RSSFeedParser(cache_dir=self.temp_dir)
        
        # Sample feedparser result (simplified)
        self.mock_feed = MagicMock()
        self.mock_feed.feed = {
            'title': 'Test Podcast',
            'description': 'Test Description',
            'link': 'https://example.com',
            'image': {'href': 'https://example.com/image.jpg'},
            'language': 'en',
            'author': 'Test Author'
        }
        self.mock_feed.entries = [
            {
                'title': 'Episode 1',
                'description': 'Episode 1 Description',
                'published': 'Mon, 01 Jan 2023 12:00:00 +0000',
                'itunes_duration': '30:00',
                'link': 'https://example.com/episode1',
                'enclosures': [
                    {'type': 'audio/mpeg', 'href': 'https://example.com/episode1.mp3'}
                ]
            }
        ]
    
    @patch('feedparser.parse')
    def test_parse_feed(self, mock_parse):
        """Test parsing an RSS feed."""
        # Setup mock
        mock_parse.return_value = self.mock_feed
        
        # Test parsing feed
        feed_url = 'https://example.com/feed.xml'
        result = self.parser.parse_feed(feed_url)
        
        # Verify results
        self.assertEqual(result['title'], 'Test Podcast')
        self.assertEqual(result['author'], 'Test Author')
        self.assertEqual(len(result['episodes']), 1)
        self.assertEqual(result['episodes'][0]['title'], 'Episode 1')
        self.assertEqual(result['episodes'][0]['audio_url'], 'https://example.com/episode1.mp3')
        
        # Verify mock was called
        mock_parse.assert_called_once_with(feed_url)
    
    @patch('feedparser.parse')
    def test_get_feeds_from_list(self, mock_parse):
        """Test parsing multiple RSS feeds."""
        # Setup mock
        mock_parse.return_value = self.mock_feed
        
        # Test parsing feeds
        feed_urls = [
            'https://example.com/feed1.xml',
            'https://example.com/feed2.xml'
        ]
        results = self.parser.get_feeds_from_list(feed_urls)
        
        # Verify results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['title'], 'Test Podcast')
        self.assertEqual(results[1]['title'], 'Test Podcast')
        
        # Verify mock was called
        self.assertEqual(mock_parse.call_count, 2)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)

class TestPodcastDownloader(unittest.TestCase):
    """Tests for the PodcastDownloader class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_audio_dir = tempfile.mkdtemp()
        self.temp_metadata_dir = tempfile.mkdtemp()
        self.downloader = PodcastDownloader(
            audio_dir=self.temp_audio_dir,
            metadata_dir=self.temp_metadata_dir
        )
        
        # Sample podcast data
        self.podcast_data = {
            'title': 'Test Podcast',
            'description': 'Test Description',
            'author': 'Test Author',
            'episodes': [
                {
                    'title': 'Episode 1',
                    'description': 'Episode 1 Description',
                    'audio_url': 'https://example.com/episode1.mp3'
                }
            ]
        }
    
    @patch('requests.get')
    def test_download_episode(self, mock_get):
        """Test downloading a podcast episode."""
        # Setup mock
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.iter_content.return_value = [b'test data']
        mock_get.return_value = mock_response
        
        # Test downloading episode
        result = self.downloader.download_episode(
            podcast_name='Test Podcast',
            episode_title='Episode 1',
            audio_url='https://example.com/episode1.mp3'
        )
        
        # Verify result
        self.assertIsNotNone(result)
        self.assertTrue(os.path.exists(result))
        
        # Verify mock was called
        mock_get.assert_called_once()
    
    @patch.object(PodcastDownloader, 'download_episode')
    def test_download_podcast(self, mock_download_episode):
        """Test downloading a podcast."""
        # Setup mock
        mock_download_episode.return_value = os.path.join(self.temp_audio_dir, 'Test_Podcast/Episode_1.mp3')
        
        # Test downloading podcast
        results = self.downloader.download_podcast(self.podcast_data, limit=1)
        
        # Verify results
        self.assertEqual(len(results), 1)
        
        # Verify metadata was saved
        metadata_path = os.path.join(self.temp_metadata_dir, 'Test_Podcast.json')
        self.assertTrue(os.path.exists(metadata_path))
        
        # Verify mock was called
        mock_download_episode.assert_called_once()
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_audio_dir)
        shutil.rmtree(self.temp_metadata_dir)

if __name__ == '__main__':
    unittest.main() 