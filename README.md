# Streamlit Text Rewrite App

A Streamlit application for text rewriting and analysis.

## Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your environment variables
4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Deployment on Streamlit Cloud

1. Fork/push this repository to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Deploy the app by connecting to your GitHub repository
4. In the Streamlit Cloud dashboard:
   - Set up your environment variables in "Advanced Settings" → "Secrets"
   - Make sure to add all the necessary API keys and configurations

## Environment Variables Required

- `GOOGLE_API_KEY`: Your Google API key for the Generative AI service
- Add any other environment variables your app needs

## Features

- Text rewriting
- Usage statistics
- History tracking
- User authentication 