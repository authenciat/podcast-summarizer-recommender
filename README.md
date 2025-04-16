# Podcast Summarizer & Recommender

An NLP tool that transcribes, summarizes, and recommends podcasts based on user interests. This project helps podcast enthusiasts discover relevant content more efficiently by automatically processing podcast episodes and providing concise summaries and personalized recommendations.

## Team Members
- Authencia Tioanda - Transcription & Topic Modeling
- Vaidehi Patil - Summarization & Web Interface

## Features

- **Podcast Collection**: Download episodes from RSS feeds
- **Custom Transcription**: Phoneme-based ASR system for speech-to-text conversion
- **Abstractive Summarization**: T5-based model to generate concise summaries
- **Topic Extraction**: BERTopic for identifying key topics and themes
- **Recommendation Engine**: Hybrid content-based and collaborative filtering
- **Web Interface**: Browse summaries and get personalized recommendations

## Project Setup

### Prerequisites

- Python 3.8+
- Required libraries (install using `pip install -r requirements.txt`)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/podcast-summarizer-recommender.git
   cd podcast-summarizer-recommender
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### Collecting Podcast Data

To collect podcast episodes from RSS feeds:

```bash
python app.py collect --feed-file feeds.json --limit 3
```

Where:
- `--feed-file` specifies a JSON file containing RSS feed URLs
- `--limit` sets the maximum number of episodes to download per podcast

Alternatively, you can specify feed URLs directly:

```bash
python app.py collect --feeds "https://feeds.npr.org/510289/podcast.xml" "https://feeds.simplecast.com/54nAGcIl" --limit 2
```

#### Other Components (Under Development)

- Transcription: Converting podcast audio to text
- Summarization: Generating concise summaries of transcripts
- Topic Modeling: Extracting key topics and themes
- Recommendation: Suggesting similar podcasts
- Web Interface: Browsing summaries and getting recommendations

## Project Structure

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
│   ├── transcription/             # Transcription modules
│   ├── summarization/             # Summarization modules
│   ├── topic_modeling/            # Topic modeling modules
│   ├── recommendation/            # Recommendation modules
│   └── web/                       # Web interface
│
├── notebooks/                     # Jupyter notebooks for experiments
├── tests/                         # Unit tests
├── models/                        # Saved model checkpoints
├── app.py                         # Main application entry point
└── requirements.txt               # Dependencies
```

## Development Roadmap

1. **Phase 1**: Setup and Data Collection
2. **Phase 2**: Core Model Development (Transcription & Summarization)
3. **Phase 3**: Feature Extraction and Recommendation
4. **Phase 4**: Web Interface Development
5. **Phase 5**: Testing and Refinement

## Contributing

This is an academic project, but contributions and suggestions are welcome. Please feel free to open an issue or submit a pull request.

## License

[MIT License](LICENSE)
