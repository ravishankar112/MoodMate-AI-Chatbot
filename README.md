# MoodMate AI -- Personality-Based AI Chatbot

MoodMate AI is a personality-based chatbot powered by **Google Gemini**,
**LangChain**, and **Streamlit**. It lets users chat with an AI
assistant in different moods through a clean, interactive web interface.

## Features

-   **Three AI personalities:** Angry, Funny, and Sad.
-   **Google Gemini integration** using LangChain.
-   **Conversation memory** during the current Streamlit session.
-   **Regenerate response** to get another answer.
-   **Search chat history**.
-   **Download conversations** as TXT or JSON.
-   **Download individual AI responses**.
-   **Suggested prompts** to start a conversation.
-   **New Chat** and **Clear Conversation** controls.
-   Modern, responsive Streamlit interface.

## Tech Stack

  Technology      Purpose
  --------------- -------------------------------
  Python          Application logic
  Streamlit       Web interface
  Google Gemini   Large language model
  LangChain       Model and message integration
  python-dotenv   Load environment variables

## Project Structure

``` text
MoodMate-AI/
├── app.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository

``` bash
git clone https://github.com/ravishankar112/MoodMate-AI.git
cd MoodMate-AI
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

``` powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure your Gemini API key

Create a `.env` file in the project folder and add:

``` env
GOOGLE_API_KEY=your_gemini_api_key_here
```

Get an API key from [Google AI
Studio](https://aistudio.google.com/apikey).

**Important:** Never upload your `.env` file or expose your API key on
GitHub.

### 5. Run the application

``` bash
streamlit run app.py
```

The app will open in your browser.

## AI Personalities

  -----------------------------------------------------------------------
  Mode                                Behavior
  ----------------------------------- -----------------------------------
  Angry                               Responds in a deliberately
                                      irritated and blunt style while
                                      remaining helpful and safe.

  Funny                               Uses humor, playful language, and
                                      light-hearted responses.

  Sad                                 Uses a gentle, emotional, and
                                      empathetic tone.
  -----------------------------------------------------------------------

## How It Works

1.  The user selects an AI personality.
2.  The user enters a message in the chat interface.
3.  LangChain sends the conversation context and personality
    instructions to Google Gemini.
4.  Gemini generates a response in the selected style.
5.  Streamlit displays the response and keeps the conversation in
    session state.

Conversation history is stored in the active Streamlit session. It is
not permanent database storage.

## Environment and Security

-   Keep API keys in `.env` or Streamlit secrets.
-   Add `.env`, virtual environments, and cache files to `.gitignore`.
-   Do not commit private credentials to GitHub.

## Future Improvements

-   Voice input and text-to-speech.
-   More chatbot personalities.
-   Persistent conversation storage with a database.
-   User authentication.
-   Streaming responses.
-   Cloud deployment.

## Developer

**Ravi Shankar Kumar**

-   GitHub: [ravishankar112](https://github.com/ravishankar112)

------------------------------------------------------------------------

If you find this project useful, feel free to star the repository.
