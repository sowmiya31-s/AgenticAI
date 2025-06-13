import streamlit as st
import google.generativeai as genai

# 🔐 Gemini API key (fixed in code)
GEMINI_API_KEY = "AIzaSyCL6YH9Oji5IWPNIriG_FejN2IzKZfE1LE"
genai.configure(api_key=GEMINI_API_KEY)

# Load the Gemini model
try:
    model = genai.GenerativeModel("gemini-2.0-flash")
except Exception as e:
    st.error(f"Error loading Gemini model: {e}")
    st.stop()

# 🌍 Streamlit UI setup
st.set_page_config(page_title="English Translator", page_icon="🌐")
st.title("🌐 English Translator")
st.write("Translate an English sentence into your chosen language using Google Gemini.")

# 🔽 Language selection
language_options = ["Hindi", "French", "Tamil", "Spanish", "German", "Japanese"]
selected_language = st.selectbox("Select target language:", language_options)

# ✏️ Input field
user_input = st.text_input("Enter your sentence in English:", placeholder="e.g., How are you?")

# 🔘 Translate button
if st.button("Translate"):
    if user_input.strip() == "":
        st.warning("Please enter a sentence.")
    else:
        with st.spinner("Translating..."):
            try:
                prompt = f"Translate the following English sentence to {selected_language}:\n\n{user_input}"
                response = model.generate_content(prompt)
                translation = response.text
                st.success(f"Translation to {selected_language} complete! 🎉")
                st.text_area(f"{selected_language} Translation:", translation, height=100)
            except Exception as e:
                st.error(f"Translation failed: {e}")
