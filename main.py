import streamlit as st
from PyPDF2 import PdfReader
from openai import OpenAI
import os
import re
import sys

# --- OPENAI CLIENT ---
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Resume Match Analyzer", layout="wide")

# --- HEADER ---
st.title("🚀 AI Resume Match Analyzer")
st.caption("Smart AI feedback for job matching and ATS optimization")
st.divider()

# --- AI FUNCTION ---
def analyze_resume(resume_text, job_text):
    prompt = f"""
You are an expert recruiter and ATS system.

Analyze this resume against the job description.

Resume:
{resume_text}

Job Description:
{job_text}

Return structured output:

Match Score: (number %)
Strengths:
Missing Skills:
Improvements:
ATS Optimization Tips:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# --- INPUT SECTION ---
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type="pdf")

with col2:
    job_desc = st.text_area("💼 Paste Job Description", height=200)

# --- ANALYZE BUTTON ---
if st.button("🚀 Analyze Resume"):

    if uploaded_file is not None and job_desc.strip() != "":

        # --- EXTRACT TEXT ---
        reader = PdfReader(uploaded_file)
        resume_text = ""

        for page in reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text

        # --- AI CALL ---
        with st.spinner("Analyzing with AI..."):
            result = analyze_resume(resume_text, job_desc)

        st.success("Analysis complete!")

        # --- RESULTS ---
        st.divider()
        st.subheader("📊 AI Analysis Results")

        # --- SCORE EXTRACTION ---
        match = re.search(r'(\d+)', result)
        score = int(match.group(1)) if match else 50

        st.metric("🎯 Match Score", f"{score}%")
        st.progress(score / 100)

        st.divider()

        # --- SECTIONS ---
        sections = {
            "💪 Strengths": "Strengths:",
            "⚠️ Missing Skills": "Missing Skills:",
            "🛠 Improvements": "Improvements:",
            "📄 ATS Tips": "ATS Optimization Tips:"
        }

        for title, key in sections.items():
            st.subheader(title)

            part = result.split(key)
            if len(part) > 1:
                content = part[1].split("\n\n")[0]
                st.write(content.strip())
            else:
                st.write("Not found")

        # --- DOWNLOAD ---
        st.divider()
        st.download_button(
            "📥 Download Report",
            result,
            file_name="resume_analysis.txt"
        )

    else:
        st.warning("Please upload a resume and paste a job description.")


# --- REPLIT FIX (DO NOT TOUCH) ---
