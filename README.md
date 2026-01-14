# 🚀 VC Pitch Deck Analyzer

Automated AI-powered pitch deck analysis system with CI/CD pipeline.

## 🎯 Features

- 📄 **PDF Analysis**: Extracts and analyzes pitch deck content
- 🤖 **AI Integration**: Uses Ollama for intelligent analysis
- 🐳 **Containerized**: Docker + Docker Compose setup
- 🔄 **CI/CD**: GitHub Actions automation
- 📊 **Monitoring**: Prometheus metrics integration
- ✅ **Testing**: Automated pytest suite

## 🏗️ Architecture
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   PDF Input │────▶│   Analyzer  │────▶│  AI Model   │
└─────────────┘     └─────────────┘     │  (Ollama)   │
                            │            └─────────────┘
                            ▼
                    ┌─────────────┐
                    │   Results   │
                    │    (JSON)   │
                    └─────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.10+

### Installation

1. Clone the repository:
```bash
git clone https://github.com/justautumns/vc_automation.git
cd vc_automation
```

2. Copy environment variables:
```bash
cp .env.example .env
```

3. Start with Docker Compose:
```bash
docker-compose up -d
```

4. Place PDF files in `pitch_decks/` folder

5. Run analysis:
```bash
docker-compose exec analyzer python startup_analyzer.py
```

## 🧪 Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```


## 🤖 Automation Modes

### Mode 1: Manual
```bash
docker-compose exec analyzer python startup_analyzer.py
```

### Mode 2: Auto-Watch (Local Development)
```bash
python auto_analyzer.py
# Now drop PDFs into pitch_decks/ folder - automatic analysis!
```

## 📊 Monitoring

Prometheus metrics available at: `http://localhost:8000/metrics`

## 🛠️ Tech Stack

- **Language**: Python 3.10
- **AI Model**: Ollama (TinyLlama/Mistral)
- **Containers**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Testing**: Pytest
- **Monitoring**: Prometheus

## 📝 License

MIT

## 👤 Author

Emre Yildiz - [GitHub](https://github.com/justautumns)