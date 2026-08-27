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
st.caption("Powered by Gemini 3.6 Flash")

if not api_key:
    st.error("Missing Gemini API Key. Please set it in .env or Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

languages = ["Spanish", "French", "German", "Hindi", "Japanese", "Mandarin", "Arabic", "Russian", "Portuguese", "Italian"]

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("Source Language", ["Auto-detect"] + languages)
with col2:
    target_lang = st.selectbox("Target Language", languages)

user_text = st.text_area("Enter text to translate:", height=150)

if st.button("Translate", type="primary"):
    if not user_text.strip():
        st.warning("Please enter text to translate.")
    else:
        with st.spinner("Translating..."):
            prompt = f"""
            You are a professional translator.
            Source Language: {source_lang}
            Target Language: {target_lang}

            Translate the following text accurately:
            ---
            {user_text}
            ---
            Only return the translated text without extra comments.
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