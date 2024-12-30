import streamlit as st
import hashlib

def initialize_theme():
    """Initialize theme in session state if not present"""
    if "theme" not in st.session_state:
        st.session_state.theme = "light"

def toggle_theme():
    """Toggle between light and dark theme"""
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
    st.rerun()

def apply_theme():
    """Apply the current theme"""
    theme = st.session_state.get("theme", "light")
    st.markdown(f"""
        <script>
            document.querySelector('[data-testid="stAppViewContainer"]').setAttribute('data-theme', '{theme}');
        </script>
    """, unsafe_allow_html=True)

def check_password():
    """Returns `True` if the user had the correct password."""
    initialize_theme()

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"].lower() == "admin" and \
           hashlib.sha256(str.encode(st.session_state["password"])).hexdigest() == "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9":
            st.session_state["password_correct"] = True
            st.session_state["authenticated"] = True
            del st.session_state["password"]  # Don't store password
            del st.session_state["username"]  # Don't store username
        else:
            st.session_state["password_correct"] = False

    def logout():
        """Logs out the user by resetting the session state."""
        theme = st.session_state.theme  # Save theme before clearing
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state.theme = theme  # Restore theme after clearing
        st.rerun()

    # Add custom CSS for login form and theme switch
    st.markdown("""
        <style>
        /* Login styles */
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            background: var(--background-color);
        }
        .login-header {
            text-align: center;
            margin-bottom: 20px;
        }
        .stButton button {
            width: 100%;
        }

        /* Theme switch styles */
        .theme-switch {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
            padding: 10px;
            border-radius: 8px;
            background: var(--background-color);
        }
        .theme-switch-icon {
            font-size: 20px;
        }
        
        /* Theme variables */
        [data-theme="light"] {
            --background-color: #ffffff;
            --text-color: #333333;
        }
        [data-theme="dark"] {
            --background-color: #2d2d2d;
            --text-color: #ffffff;
        }
        </style>
    """, unsafe_allow_html=True)

    # Apply current theme
    apply_theme()

    if "authenticated" not in st.session_state:
        # First run, show inputs for username + password.
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div class="login-header">', unsafe_allow_html=True)
        st.markdown("### 🔐 Login Required")
        st.markdown("</div>", unsafe_allow_html=True)
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        st.button("Login", on_click=password_entered)
        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.error("😕 Invalid username or password")
        st.markdown("</div>", unsafe_allow_html=True)
        return False
    
    # Add theme switch and logout button in sidebar if authenticated
    if st.session_state.get("authenticated", False):
        with st.sidebar:
            # Theme switch
            st.markdown('<div class="theme-switch">', unsafe_allow_html=True)
            current_theme = st.session_state.theme
            theme_icon = "🌙" if current_theme == "light" else "☀️"
            theme_text = "Dark Mode" if current_theme == "light" else "Light Mode"
            if st.button(f"{theme_icon} Switch to {theme_text}"):
                toggle_theme()
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Logout button
            st.button("Logout", on_click=logout)
        return True
    
    return False 