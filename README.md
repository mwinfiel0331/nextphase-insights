# NextPhase Insights

Process optimization platform built with Streamlit and Firebase.

## Features

- 📊 Real-time process optimization dashboard
- 📝 Client intake management
- 📅 Session tracking and progress monitoring
- 🔒 Secure data storage with Firebase
- 📈 Data visualization and analytics

## Prerequisites

- Python 3.9+
- Firebase project credentials
- Streamlit 1.27.0+
- Firebase Admin SDK

## Installation

1. Clone the repository:
```powershell
git clone https://github.com/yourusername/nextphase-insights.git
cd nextphase-insights
```

2. Install dependencies:
```powershell
pip install -r requirements.txt
```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your Firebase credentials

## Project Structure

```
nextphase-insights/
├── src/
│   ├── pages/           # Application pages
│   ├── services/        # Database and auth services
│   └── utils/           # Utility functions
├── tests/               # Test files
├── app.py              # Main application
├── requirements.txt    # Dependencies
└── README.md          # This file
```

## Running the Application

```powershell
streamlit run app.py
```

## Development

1. Create virtual environment:
```powershell
python -m venv env
.\env\Scripts\activate
```

2. Install dev dependencies:
```powershell
pip install -r requirements-dev.txt
```

## Security

- Environment-based configuration
- Secure credential management
- Firebase security rules

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature/name`
5. Submit pull request

## Version History

See [CHANGELOG.md](CHANGELOG.md) for version details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/)
- [Firebase](https://firebase.google.com/)
- [Plotly](https://plotly.com/)
