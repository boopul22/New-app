import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit.components.v1 as components
from auth import check_password
from user_data import UserHistory
import time

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Set page configuration
st.set_page_config(
    page_title="AI Text Rewriter",
    page_icon="🤖",
    layout="wide"
)

def show_loading_message():
    with st.spinner("🤖 Ruko jara... Sabar ka phal meetha hota hai"):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)

# Check authentication before showing anything
if check_password():
    # Add custom CSS
    st.markdown("""
        <style>
        /* Base styles */
        .stTextArea textarea {
            font-size: 16px;
            border-radius: 12px;
            border: 1px solid var(--border-color, #e0e0e0);
            min-height: 150px;
            width: 100% !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            background-color: var(--background-color) !important;
            color: var(--text-color) !important;
        }

        /* Header styles */
        .header {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 1rem 0;
            margin-bottom: 2rem;
            color: var(--text-color);
        }
        .header h1 {
            font-size: 24px;
            font-weight: 600;
            margin: 0;
        }

        /* Theme variables */
        [data-theme="light"] {
            --background-color: #ffffff;
            --text-color: #333333;
            --border-color: #e0e0e0;
        }
        [data-theme="dark"] {
            --background-color: #2d2d2d;
            --text-color: #ffffff;
            --border-color: #4a4a4a;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
        <div class="header">
            <span style="font-size: 24px;">🤖</span>
            <h1>AI Text Rewriter</h1>
        </div>
    """, unsafe_allow_html=True)

    def rewrite_text(input_text):
        try:
            # Create the model
            generation_config = {
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }

            model = genai.GenerativeModel(
                model_name="gemini-2.0-flash-exp",
                generation_config=generation_config,
            )

            chat_session = model.start_chat(history=[])
            
            # Show loading message while processing
            with st.spinner("🤖 Ruko jara... Sabar ka phal meetha hota hai"):
                # Construct the prompt
                prompt = f'''make this in very natural language that normal man speck in active voice in hindi just provide the output text:

                {input_text}'''
                
                # Get response from Gemini
                response = chat_session.send_message(prompt)
                
                # Add to history when successful
                if response.text:
                    user_history = UserHistory()
                    user_history.add_entry(input_text, response.text)
                    
                return response.text
        except Exception as e:
            return None

    # Original text input
    st.markdown("**Original Text**")
    input_text = st.text_area(
        "",
        height=150,
        placeholder="Enter the text you want to rewrite..."
    )

    # Center the rewrite button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("✨ Rewrite Text", type="primary", use_container_width=True):
            st.session_state.button_clicked = True
            st.session_state.processing = True

    # Main interface
    if 'button_clicked' in st.session_state and st.session_state.button_clicked:
        if input_text:
            if st.session_state.get('processing', False):
                rewritten_text = rewrite_text(input_text)
                if rewritten_text:
                    st.session_state.processing = False
                    st.session_state.result = rewritten_text
                    st.rerun()
                else:
                    st.error("😕 Something went wrong. Please try again.")
                    st.session_state.processing = False
            
            if not st.session_state.get('processing', False):
                rewritten_text = st.session_state.get('result', '')
                if rewritten_text:
                    st.text_area(
                        "",
                        value=rewritten_text,
                        height=150,
                        key="rewritten_text"
                    )
                    components.html("""
                        <div class="copy-button-container">
                            <button onclick="copyText()" class="copy-button">
                                📋 Copy Text
                            </button>
                        </div>
                        <script>
                            function copyText() {
                                const textArea = document.querySelector('textarea[data-testid="stTextArea"]');
                                textArea.select();
                                textArea.setSelectionRange(0, 99999);
                                navigator.clipboard.writeText(textArea.value);
                                const notification = document.createElement('div');
                                notification.style.position = 'fixed';
                                notification.style.bottom = '20px';
                                notification.style.right = '20px';
                                notification.style.background = '#4CAF50';
                                notification.style.color = 'white';
                                notification.style.padding = '12px 24px';
                                notification.style.borderRadius = '8px';
                                notification.style.boxShadow = '0 2px 4px rgba(0,0,0,0.2)';
                                notification.textContent = '✓ Copied to clipboard!';
                                document.body.appendChild(notification);
                                setTimeout(() => notification.remove(), 3000);
                            }
                        </script>
                    """, height=70)
        else:
            st.warning("Please enter some text to rewrite.")
    else:
        st.text_area(
            "",
            value="Your rewritten text will appear here...",
            height=150,
            key="rewritten_text_placeholder",
            disabled=True
        ) 