# Thoughtful AI Customer Support Agent

A conversational AI agent built with Streamlit that answers questions about Thoughtful AI's automation agents. The agent uses fuzzy matching for predefined questions and falls back to OpenAI's GPT for general queries.

## Features

- **Predefined Q&A**: Answers common questions about Thoughtful AI's agents (EVA, CAM, PHIL)
- **Fuzzy Matching**: Intelligently matches user questions even with typos or variations
- **OpenAI Fallback**: Uses GPT for questions outside the predefined dataset
- **Chat Interface**: Clean, conversational UI powered by Streamlit
- **Error Handling**: Gracefully handles API failures and invalid inputs

## Setup

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. Clone this repository or download the files

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

4. Add your OpenAI API key to the `.env` file:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser to the URL shown (typically `http://localhost:8501`)

3. Start chatting with the agent!

## Example Questions

Try asking:
- "What does EVA do?"
- "Tell me about Thoughtful AI's agents"
- "How does PHIL work?"
- "What are the benefits of using your agents?"
- Or any general question!

## How It Works

1. **Fuzzy Matching**: The agent first compares your question against predefined questions using fuzzy string matching (70% similarity threshold)
2. **Predefined Response**: If a match is found, it returns the corresponding answer from the dataset
3. **OpenAI Fallback**: If no match is found, the question is sent to OpenAI's GPT for a general response
4. **Error Handling**: All API calls and user inputs are validated with appropriate error messages

## Project Structure

```
.
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create from .env.example)
├── .env.example       # Template for environment variables
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Technologies Used

- **Streamlit**: Web UI framework
- **OpenAI API**: GPT-powered fallback responses
- **RapidFuzz**: Fuzzy string matching
- **Python-dotenv**: Environment variable management

## License

This project is created as a coding challenge for Thoughtful AI.

