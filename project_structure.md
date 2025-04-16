# Podcast Summarizer & Recommender - Project Structure

```
podcast-summarizer-recommender/
│
├── data/                          # Data storage
│   ├── raw/                       # Raw podcast audio files
│   ├── transcriptions/            # Generated transcriptions
│   ├── summaries/                 # Generated summaries
│   └── metadata/                  # Podcast metadata
│
├── src/                           # Source code
│   ├── data_collection/           # Data collection modules
│   │   ├── __init__.py
│   │   ├── rss_feed.py            # RSS feed parser
│   │   ├── podcast_downloader.py  # Audio downloading utilities
│   │   └── metadata_collector.py  # Collect podcast metadata
│   │
│   ├── transcription/             # Transcription modules (Authencia)
│   │   ├── __init__.py
│   │   ├── audio_preprocessor.py  # Audio preprocessing
│   │   ├── phoneme_recognizer.py  # Custom phoneme recognition
│   │   └── asr_model.py           # Speech recognition model
│   │
│   ├── summarization/             # Summarization modules (Vaidehi)
│   │   ├── __init__.py
│   │   ├── text_preprocessor.py   # Text preprocessing
│   │   ├── t5_model.py            # T5 model implementation
│   │   └── summarizer.py          # Summarization pipeline
│   │
│   ├── topic_modeling/            # Topic modeling modules (Authencia)
│   │   ├── __init__.py
│   │   ├── bertopic_model.py      # BERTopic implementation
│   │   └── topic_extractor.py     # Topic extraction utilities
│   │
│   ├── recommendation/            # Recommendation modules (Both)
│   │   ├── __init__.py
│   │   ├── content_based.py       # Content-based filtering
│   │   ├── collaborative.py       # Collaborative filtering
│   │   └── recommender.py         # Hybrid recommendation system
│   │
│   └── web/                       # Web interface (Vaidehi)
│       ├── __init__.py
│       ├── app.py                 # Flask application
│       ├── routes.py              # API routes
│       ├── static/                # Static files (CSS, JS)
│       └── templates/             # HTML templates
│
├── notebooks/                     # Jupyter notebooks for experiments
│   ├── data_exploration.ipynb
│   ├── transcription_tests.ipynb
│   ├── summarization_tests.ipynb
│   └── recommendation_tests.ipynb
│
├── tests/                         # Unit tests
│   ├── test_transcription.py
│   ├── test_summarization.py
│   ├── test_topic_modeling.py
│   └── test_recommendation.py
│
├── models/                        # Saved model checkpoints
│   ├── transcription/
│   ├── summarization/
│   └── topic/
│
├── app.py                         # Main application entry point
├── config.py                      # Configuration parameters
├── requirements.txt               # Dependencies
└── README.md                      # Project documentation
```

## Development Roadmap

### Phase 1: Setup and Data Collection
- Set up project structure
- Implement RSS feed parsing and podcast downloading
- Collect initial dataset for model development

### Phase 2: Core Model Development
- Authencia: Develop custom ASR system for transcription
- Vaidehi: Implement and fine-tune T5 model for summarization
- Set up evaluation metrics for both systems

### Phase 3: Feature Extraction and Recommendation
- Implement BERTopic for topic modeling
- Develop similarity metrics for podcast content
- Create hybrid recommendation system

### Phase 4: Web Interface
- Develop Flask backend
- Create user interface for browsing and recommendations
- Integrate all components

### Phase 5: Testing and Refinement
- Test system with real users
- Refine models based on feedback
- Optimize for performance 