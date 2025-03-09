import streamlit as st
import json
import os
import re
import random
import string

# File to store saved credentials
CREDENTIALS_FILE = "credentials.json"

# Function to generate a random password
def generate_password(length=8, use_digits=True, use_special=True):
    characters = string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Function to check password strength
def check_password_strength(password):
    common_passwords = ["password123", "abcdef", "assign03", "123", "admin", "maeyda"]

    if password in common_passwords:
        return "❌ This password is too common. Choose a more unique one.", "Weak"
    
    score = 0
    tips = []

    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        tips.append("❌ Password should be at least 8 characters long.")

    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        tips.append("❌ Include both uppercase and lowercase letters.")

    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        tips.append("❌ Add at least one number (0-9).")

    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        tips.append("❌ Include at least one special character (!@#$%^&*).")

    # Strength Rating
    if score == 4:
        return "✅ Strong Password!", "Strong"
    elif score == 3:
        return "⚠️ Moderate Password - Consider adding more security features.", "Moderate"
    else:
        return "\n".join(tips), "Weak"

# Function to load stored credentials
def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    return {}

# Function to save credentials
def save_credentials(credentials):
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(credentials, file, indent=4)

# Load existing credentials
credentials = load_credentials()

# Initialize session state for email history
if "email_history" not in st.session_state:
    st.session_state.email_history = list(credentials.keys())

st.image("icon.png", width=150)

st.title("🔐 Secure Login Page")
st.markdown(
    """
    <style>
    input[type="text"], input[type="password"] {
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Single email input with suggestions (simulated using placeholders)
email_placeholder = "Enter your email..."
email_suggestions = "\n".join(st.session_state.email_history)  # Joining emails as a list

email = st.text_input("📧 Email", placeholder=email_placeholder, value="", help=f"Suggestions:\n{email_suggestions}")

# Autofill password if email exists
password_placeholder = ""
if email in credentials:
    st.info("✅ Existing user detected. Autofilling password...")
    password_placeholder = credentials[email]

password = st.text_input("🔑 Password", value=password_placeholder, type="password")

# Password strength check
if password:
    result, strength = check_password_strength(password)
    if strength == "Strong":
        st.success(result)
        st.balloons()
    elif strength == "Moderate":
        st.warning(result)
    else:
        st.error("❌ Weak Password - Improve it using these tips:")
        for tip in result.split("\n"):
            st.write(tip)

remember_me = st.checkbox("💾 Remember Me")

st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Login button
if st.button("🔓 Login"):
    if email and password:
        if email in credentials and credentials[email] == password:
            st.success(f"🎉 Welcome back, {email}!")
        else:
            st.warning("🛑 Incorrect email or password!")

        # Store credentials if "Remember Me" is checked
        if remember_me:
            credentials[email] = password
            save_credentials(credentials)

            # Add email to session state history
            if email not in st.session_state.email_history:
                st.session_state.email_history.append(email)

            st.info("🔒 Password saved securely!")
    else:
        st.error("⚠️ Please enter both email and password")

# Password generator
password_length = st.number_input("Choose password length:", min_value=8, max_value=20, value=12)
if st.button("Generate Strong Password"):
    strong_password = generate_password(password_length)
    st.text_input("Suggested Strong Password:", strong_password)
