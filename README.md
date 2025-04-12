# NextPhase Insights

Process optimization and workflow management platform.

## 🚀 Features

### Admin Dashboard
- User management with status control
- Process intake review system
- Real-time metrics and analytics
- Workflow status tracking

### Client Intake System
- Multi-step intake form with progress tracking
- Tool and system assessment
- Process documentation upload
- Draft saving and review capabilities

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key
- Firebase account
- Git

## 🛠️ Setup and Installation

## Clone and setup:
```powershell
git clone https://github.com/yourusername/nextphase-insights.git
cd nextphase-insights
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Configure the Environment
```properties
# .env file
OPENAI_API_KEY=your_openai_key
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_CLIENT_EMAIL=your_service_account_email
FIREBASE_PRIVATE_KEY=your_private_key
```
## Database Initialization

The application requires two initialization steps:

### Initialize Database Structure

Run the database initialization script to create collections and base documents:

```powershell
python -m scripts.init.run_init
```

This will:
- Set up Firebase connection
- Create required collections
- Add metadata documents
- Configure base settings

### Create Database Indexes

Run the index management script to create required Firestore indexes:

```powershell
python scripts/manage_indexes.py
```

This will:
- Create composite indexes for queries
- Set up query optimization
- Enable sorting and filtering

## 📊 Dashboard Access

### Admin Dashboard
Access the admin dashboard by logging in with admin credentials:
```powershell
streamlit run app.py
```

Admin features include:
- User management
- Intake form review
- Process analysis
- System metrics

### Client Dashboard
Regular users will see:
- Intake form submission
- Process status tracking
- Documentation management

## Running the Application

Start the Streamlit server:

```powershell
streamlit run app.py
```

## 🐛 Bug Reporting
Submit bugs using GitHub CLI:
```powershell
gh issue create -F .github/ISSUE_TEMPLATE/bug.md --label "bug"
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

## 📝 Documentation
- [Changelog](CHANGELOG.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Firebase Docs](https://firebase.google.com/docs)
- [Streamlit Docs](https://docs.streamlit.io/)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Reporting Issues
Please check the [Known Issues](BUGS.md) document before reporting new bugs. For new issues, use the GitHub Issues template and include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Impact assessment

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📈 Version History

See [CHANGELOG.md](CHANGELOG.md) for release details.
