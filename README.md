# YapYard

YapYard is an AI-powered application built with Streamlit that provides secure access to AI agents through authentication. The application features:

- Secure login system with API key validation
- Integration with GROQ API for AI capabilities
- Customizable AI agent management

## Features

- User authentication with username/password and API key validation
- Session management for secure API key storage
- Logout functionality
- Agent management interface

## Getting Started

### Prerequisites

- Python 3.8+
- Streamlit
- GROQ API key (stored in .env file)

### Installation

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your GROQ_API_KEY

### Usage

1. Run the application:
   ```bash
   streamlit run app.py
   ```
2. Access the application in your browser
3. Login with your credentials and API key

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](LICENSE)