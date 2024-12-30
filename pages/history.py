import streamlit as st
from datetime import datetime
from auth import check_password
from user_data import UserHistory

# Set page configuration
st.set_page_config(
    page_title="History - Text Rewriter",
    page_icon="📚",
    layout="wide"
)

# Check authentication before showing anything
if check_password():
    # Add custom CSS with theme-aware colors
    st.markdown("""
        <style>
        /* Base styles */
        body {
            background-color: transparent;
        }
        .stTextArea textarea {
            font-size: 16px;
            border-radius: 12px;
            border: 1px solid var(--border-color, #e0e0e0);
            min-height: 100px;
            width: 100% !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            background-color: var(--textarea-bg, #ffffff) !important;
            color: var(--text-color, #333333) !important;
            padding: 8px;
        }
        
        /* Card styles */
        .card {
            background: var(--card-bg, #ffffff);
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 12px;
            border: 1px solid var(--border-color, #e0e0e0);
            color: var(--text-color);
        }
        .card h1 {
            color: #2196F3;
            margin-bottom: 0.5rem;
            font-weight: 700;
            text-align: center;
        }
        .card h3 {
            color: var(--text-color);
            margin-bottom: 1rem;
        }
        .subtitle {
            text-align: center;
            color: var(--text-color);
            font-size: 1rem;
            margin-bottom: 1rem;
        }
        
        /* Theme-aware colors */
        [data-testid="stAppViewContainer"] {
            --border-color: var(--primary-border-color);
            --card-bg: var(--primary-card-bg);
            --text-color: var(--primary-text-color);
            --textarea-bg: var(--primary-textarea-bg);
        }
        
        /* Light theme */
        [data-theme="light"] {
            --primary-border-color: #e0e0e0;
            --primary-card-bg: #ffffff;
            --primary-text-color: #333333;
            --primary-textarea-bg: #ffffff;
        }
        
        /* Dark theme */
        [data-theme="dark"] {
            --primary-border-color: #4a4a4a;
            --primary-card-bg: #2d2d2d;
            --primary-text-color: #ffffff;
            --primary-textarea-bg: #1e1e1e;
        }

        /* Fix for markdown text colors */
        [data-testid="stMarkdownContainer"] {
            color: var(--text-color) !important;
        }
        
        /* Fix for text area labels */
        .stTextArea label {
            color: var(--text-color) !important;
        }

        /* Fix for disabled text areas */
        .stTextArea textarea:disabled {
            opacity: 0.7;
            color: var(--text-color) !important;
            background-color: var(--textarea-bg) !important;
        }
        </style>

        <script>
            // Theme detection
            const detectTheme = () => {
                const isDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
                document.querySelector('[data-testid="stAppViewContainer"]').setAttribute('data-theme', isDark ? 'dark' : 'light');
            }
            
            // Run on load
            detectTheme();
            
            // Watch for theme changes
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', detectTheme);
        </script>
    """, unsafe_allow_html=True)

    # Title and description
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("📚 Rewrite History")
    st.markdown('<p class="subtitle">View your previous text rewrites</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Initialize user history
    user_history = UserHistory()

    # Display history
    history_entries = user_history.get_history()
    if history_entries:
        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            for entry in reversed(history_entries):
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(f"### 🕒 {entry['timestamp']}")
                
                # Original text
                st.markdown("**Original Text:**")
                st.text_area(
                    "",
                    value=entry['original'],
                    height=80,
                    key=f"hist_orig_{entry['timestamp']}",
                    disabled=True
                )
                
                # Rewritten text
                st.markdown("**Rewritten Text:**")
                st.text_area(
                    "",
                    value=entry['rewritten'],
                    height=80,
                    key=f"hist_rew_{entry['timestamp']}",
                    disabled=True
                )
                st.markdown('</div>', unsafe_allow_html=True)
                
            # Clear history button
            if st.button("🗑️ Clear All History", type="primary"):
                user_history.clear_history()
                st.rerun()
    else:
        st.info("No history available yet. Your rewritten texts will appear here once you start using the Text Rewriter.") 