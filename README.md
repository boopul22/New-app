# Text Rewriter App

A Streamlit application that uses Google's Gemini API to rewrite text in a more natural, conversational style.

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your secrets:
   - For local development:
     Create `.streamlit/secrets.toml` in the root directory and add:
     ```toml
     GEMINI_API_KEY = "your_api_key_here"
     ```
   - For Streamlit Cloud deployment:
     Add your secrets in the Streamlit Cloud dashboard under "Deploy" -> "Secrets"

## Running the App

Run the following command in your terminal:
```bash
streamlit run app.py
```

The app will open in your default web browser.

## Usage

1. Enter or paste your text in the input field
2. Click the "Rewrite Text" button
3. The rewritten version will appear below

## Features

- Clean, user-friendly interface
- Real-time text rewriting using Gemini AI
- Error handling and loading states
- Responsive design 