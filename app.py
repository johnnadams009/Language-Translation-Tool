import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Read API key from environment (or Streamlit secrets when hosted)
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

st.set_page_config(page_title="AI Language Translator", page_icon="🌐", layout="centered")

st.title("🌐 AI Language Translator")
st.caption("Powered by Google Gemini")

if not api_key:
    st.error("Missing Gemini API Key. Please set it in .env or Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# Comprehensive list with major Indian languages + top global languages
languages = sorted([
    # Major Indian Languages
    "Assamese",
    "Bengali",
    "Bodo",
    "Dogri",
    "Gujarati",
    "Hindi",
    "Kannada",
    "Kashmiri",
    "Konkani",
    "Maithili",
    "Malayalam",
    "Manipuri (Meitei)",
    "Marathi",
    "Nepali",
    "Odia",
    "Punjabi",
    "Sanskrit",
    "Santali",
    "Sindhi",
    "Tamil",
    "Telugu",
    "Urdu",
    
    # Major Global Languages
    "Arabic",
    "Chinese (Simplified)",
    "Chinese (Traditional)",
    "English",
    "French",
    "German",
    "Italian",
    "Japanese",
    "Korean",
    "Portuguese",
    "Russian",
    "Spanish"
])

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("Source Language", ["Auto-detect"] + languages)
with col2:
    # Default target to Hindi if present, otherwise default to first item
    default_idx = languages.index("Hindi") if "Hindi" in languages else 0
    target_lang = st.selectbox("Target Language", languages, index=default_idx)

user_text = st.text_area("Enter text to translate:", height=150)

if st.button("Translate", type="primary"):
    if not user_text.strip():
        st.warning("Please enter text to translate.")
    else:
        with st.spinner("Translating..."):
            prompt = f"""
            You are a professional translator and linguist.
            Source Language: {source_lang}
            Target Language: {target_lang}

            Translate the following text accurately, ensuring natural phrasing, correct grammar, and preserving context:
            ---
            {user_text}
            ---
            Only return the translated text without extra introductory or concluding remarks.
            """
            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(temperature=0.3)
                )
                st.subheader("Translation:")
                st.success(response.text.strip())
            except Exception as e:
                st.error(f"Error: {e}")