# TailorTalk: Titanic Dataset Explorer

A natural language interface for exploring and analyzing the Titanic dataset. Ask questions in plain English and get insightful answers with visualizations.

## Features

- Natural language query processing
- Advanced data analysis of the Titanic dataset
- Beautiful visualizations (bar charts, histograms, scatter plots, etc.)
- Modern, minimalistic UI
- Chat history tracking

## Architecture

The application consists of two main components:

1. **Backend API (FastAPI)**: Handles natural language processing, data analysis, and visualization generation
2. **Frontend UI (Streamlit)**: Provides a user-friendly interface for interacting with the API

## Setup

### Prerequisites

- Python 3.9+
- pip
- virtualenv (recommended)

### Installation

1. Clone the repository:
 

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with the following content:
   ```
   # API Settings
   API_HOST=0.0.0.0
   API_PORT=8000
   DEBUG=True

   # Database Settings
   DATABASE_URL=sqlite:///./titanic.db

   # LLM Settings
   OPENAI_API_KEY=your_openai_api_key_here
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   USE_OPENROUTER=True
   LLM_MODEL=qwen/qwen-vl-plus:free

   # Frontend Settings
   STREAMLIT_SERVER_PORT=8502
   BACKEND_API_URL=http://localhost:8000
   ```

   Replace `your_openrouter_api_key_here` with your actual OpenRouter API key.

### Running the Application

#### Option 1: Run with a single command (Recommended)

```bash
python run.py
```

This will start both the backend and frontend servers in a single process. Press Ctrl+C to stop both servers.

#### Option 2: Run components separately

1. Start the backend server:
   ```bash
   cd app
   python main.py
   ```

2. In a new terminal, start the frontend:
   ```bash
   cd frontend
   streamlit run app.py
   ```

3. Open your browser and navigate to:
   - Frontend: http://localhost:8502
   - Backend API docs: http://localhost:8000/docs

## Usage

1. Enter your question about the Titanic dataset in the chat input field
2. The AI will analyze your question, perform the appropriate data analysis, and provide a response with visualizations
3. You can ask follow-up questions to explore the data further

### Example Questions

- What was the survival rate by passenger class?
- Show age distribution of survivors vs non-survivors
- Was fare price correlated with survival?
- Which embarking port had the highest survival rate?
- Compare survival rates between males and females
- What factors had the biggest impact on survival?

## Troubleshooting

If you encounter any issues while running the application, please refer to the [Troubleshooting Guide](TROUBLESHOOTING.md) for solutions to common problems.

### Import Error: No module named 'app'

If you encounter this error when running the backend, make sure you're running the server from the correct directory:

```bash
cd app
python main.py
```

