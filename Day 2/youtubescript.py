import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import os

# 🔐 Configure Gemini API Key (Replace with your secure key)
genai.configure(api_key="AIzaSyCL6YH9Oji5IWPNIriG_FejN2IzKZfE1LE")

# ✅ Clean Unicode Characters for PDF Output
def sanitize_text(text):
    replacements = {
        "“": "\"", "”": "\"", "’": "'", "‘": "'",
        "–": "-", "—": "-", "…": "...",
        "•": "*", "→": "->"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.encode("latin-1", "ignore").decode("latin-1")

# ✅ Gemini Script Generator
def generate_script(topic, tone, length, voice_style="Friendly", format_style="Paragraph",
                    video_type="Tutorial", language="English", include_sections=None, variation=False):
    model = genai.GenerativeModel("gemini-1.5-flash")

    include_text = ""
    if include_sections:
        if "Call to Action" in include_sections:
            include_text += "- Call to Action\n"
        if "Thumbnail Title" in include_sections:
            include_text += "- Suggested Thumbnail Title\n"
        if "Video Description" in include_sections:
            include_text += "- Suggested Video Description (SEO-friendly)\n"

    prompt = f"""
Generate a YouTube video script.

Topic: {topic}
Tone: {tone}
Voice Style: {voice_style}
Length: {'1-2 minutes' if length == 'Short' else '5-8 minutes'}
Video Type: {video_type}
Script Format: {format_style}
Language: {language}

Sections to include:
- Hook / Introduction
- Script Body
{include_text.strip()}

{'Add slight creative variation in style.' if variation else ''}
"""
    response = model.generate_content(prompt)
    return response.text

# ✅ PDF Generator (Safe for Unicode)
def generate_pdf(script_text, filename="YouTube_Script.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    script_text = sanitize_text(script_text)

    for line in script_text.split("\n"):
        if not line.strip():
            continue
        if line.lower().startswith(("hook", "script body", "call to action", "suggested thumbnail", "suggested video")):
            pdf.set_font("Arial", size=12, style="B")
        else:
            pdf.set_font("Arial", size=12, style="")
        pdf.multi_cell(0, 10, line)

    pdf.output(filename)
    return filename

# ✅ Streamlit UI Setup
st.set_page_config(page_title="🎬 YouTube Script Generator", layout="wide")
st.title("🎬 YouTube Script Generator")
st.markdown("Generate high-quality video scripts with **Gemini AI** 🚀")

# ✅ Input Section
with st.form("script_form"):
    st.subheader("📝 Script Configuration")
    col1, col2 = st.columns(2)

    with col1:
        topic = st.text_input("🎯 Enter the video topic", placeholder="e.g., How to Stay Focused While Studying")
        tone = st.radio("🎭 Select the tone", ["Educational", "Entertaining", "Inspirational"])
        voice_style = st.selectbox("🗣️ Voice Style", ["Friendly", "Professional", "Humorous", "Dramatic"])
        format_style = st.radio("📌 Script Format", ["Paragraph", "Bullet Points"])

    with col2:
        length = st.radio("⏱ Select script length", ["Short", "Long"])
        video_type = st.selectbox("🎬 Video Type", ["Tutorial", "Vlog", "Product Review", "Explainer", "Motivational"])
        language = st.selectbox("🌍 Output Language", ["English", "Tamil", "Hindi", "Spanish"])
        include_sections = st.multiselect(
            "📄 Include in Output",
            ["Call to Action", "Thumbnail Title", "Video Description"],
            default=["Call to Action", "Thumbnail Title", "Video Description"]
        )

        submitted = st.form_submit_button("🚀 Generate Script")

# ✅ Handle Form Submission
if submitted and topic.strip():
    with st.spinner("⏳ Generating script..."):
        script = generate_script(
            topic, tone, length, voice_style, format_style,
            video_type, language, include_sections
        )
        st.session_state['last_script'] = script
        st.session_state['form_data'] = {
            'topic': topic,
            'tone': tone,
            'length': length,
            'voice_style': voice_style,
            'format_style': format_style,
            'video_type': video_type,
            'language': language,
            'include_sections': include_sections
        }

# ✅ Output Display & Actions
if 'last_script' in st.session_state:
    with st.expander("📜 View Generated Script", expanded=True):
        st.markdown(st.session_state['last_script'])

    pdf_path = generate_pdf(st.session_state['last_script'])

    with st.columns([0.3, 0.3, 0.3])[1]:
        st.download_button(
            label="⬇️ Download Script as PDF",
            data=open(pdf_path, 'rb'),
            file_name="YouTube_Script.pdf",
            mime="application/pdf"
        )

    if st.button("🔁 Regenerate Script with Variation"):
        with st.spinner("🎨 Regenerating with creative variation..."):
            form_data = st.session_state['form_data']
            script = generate_script(
                form_data['topic'],
                form_data['tone'],
                form_data['length'],
                form_data['voice_style'],
                form_data['format_style'],
                form_data['video_type'],
                form_data['language'],
                form_data['include_sections'],
                variation=True
            )
            st.session_state['last_script'] = script
            st.rerun()

# ✅ Footer
st.markdown("---")
st.markdown("🧠 Powered by **Google Gemini API** | Built with ❤️ using **Streamlit**")
