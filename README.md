# NextPhase Insights

AI-powered process optimization and automation analysis platform built with Streamlit, Firebase, and OpenAI.

## 🚀 Features

- 🤖 AI-powered process analysis
- 📊 Automation potential scoring
- 💾 Intelligent caching system
- 🔄 Process optimization recommendations
- 📝 Client intake management
- 📈 Data visualization
- 🔐 Secure data storage

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key
- Firebase account
- Git

## ⚡ Quick Start

1. Clone and setup:
```powershell
git clone https://github.com/yourusername/nextphase-insights.git
cd nextphase-insights
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

2. Configure environment:
```properties
# .env file
OPENAI_API_KEY=your_openai_key
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_CLIENT_EMAIL=your_service_account_email
FIREBASE_PRIVATE_KEY=your_private_key
```

3. Run the application:
```powershell
streamlit run app.py
```

## 🔧 Usage

### Process Analysis
```python
from src.utils.ai_analyzer import ProcessAnalyzer

analyzer = ProcessAnalyzer()

# Get process recommendations
result = analyzer.get_process_recommendations(
    process_name="Invoice Processing",
    current_steps=["Manual data entry", "Email approvals"],
    industry="Finance"
)

# Calculate automation potential
score = analyzer.score_automation_potential({
    'name': 'Invoice Processing',
    'description': 'Manual invoice processing workflow',
    'tools': ['Email', 'Excel'],
    'frequency': 'Daily'
})
```

## 🧪 Testing

Run tests with coverage:
```powershell
pytest tests/ -v --cov=src
```

Generate coverage report:
```powershell
pytest tests/ --cov=src --cov-report=html
```

## 📁 Project Structure

```
nextphase-insights/
├── src/
│   ├── pages/
│   │   ├── components/
│   │   │   └── process_analyzer.py
│   │   ├── dashboard.py
│   │   └── intake_form.py
│   ├── services/
│   │   └── db_service.py
│   └── utils/
│       └── ai_analyzer.py
├── tests/
│   └── unit/
│       └── test_open_ai.py
├── .env
├── CHANGELOG.md
└── README.md
```

## 🔐 Security

- Store API keys in environment variables
- Use Firebase Authentication
- Regular API key rotation
- Rate limiting implementation
- Secure data validation

## 📚 Documentation

- [OpenAI API Docs](https://platform.openai.com/docs)
- [Firebase Docs](https://firebase.google.com/docs)
- [Streamlit Docs](https://docs.streamlit.io/)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📈 Version History

See [CHANGELOG.md](CHANGELOG.md) for release details.
