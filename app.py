from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import fitz  # PyMuPDF
import google.generativeai as genai

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        [input_text, pdf_content, prompt],
        generation_config={"temperature": 0}
    )
    return response.text

def input_pdf_setup(uploaded_file):
    """
    Extracts text content from the uploaded PDF using PyMuPDF.
    Returns the text in a string format.
    """
    if uploaded_file is not None:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        return full_text
    else:
        raise FileNotFoundError("No file uploaded")

# ------------------ CUSTOM CSS ------------------ #
st.set_page_config(page_title="Resume Screening", layout="wide")

custom_css = """
<style>
.stApp {
    background: #000000;
    color: #ffffff;
}
h1 {
    color: #ff416c;
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    margin-bottom: 1rem;
}
h2, h3, h4 {
    color: #f3f3f3;
}
.stButton > button {
    min-width: 150px;
    height: 48px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    background: linear-gradient(135deg, #ff416c, #ff4b2b);
    color: white;
    font-size: 16px;
    padding: 0.6rem 1.2rem;
    box-shadow: 3px 3px 5px rgba(255, 75, 43, 0.3);
    border: none;
    transition: all 0.3s ease;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #ff4b2b, #ff416c);
    box-shadow: 5px 5px 10px rgba(255, 75, 43, 0.5);
}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar Instructions
st.sidebar.title("Resume Screening")
st.sidebar.markdown("### How to Use:")
st.sidebar.markdown("""
1. **Enter the Job Description**.
2. **Upload multiple PDF Resumes**.
3. Click an **Analysis Button**.
4. View results for each resume separately.
""")

# --------------- MAIN TITLE --------------- #
st.markdown('<h1 style="color: #ff69b4;">📄 Resume Screening</h1>', unsafe_allow_html=True)  # hot pink


# --------------- LAYOUT: 2 COLUMNS --------------- #
col1, col2 = st.columns([2, 1])

# -------- LEFT COLUMN: JOB DESCRIPTION --------- #
with col1:
    st.markdown("### 📝 Job Description")
    input_text = st.text_area("Enter Job Description:", key="input")

# -------- RIGHT COLUMN: RESUME UPLOAD --------- #
with col2:
    st.markdown("### 📂 Upload Resumes")
    uploaded_files = st.file_uploader("Upload resumes (PDF)...", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} PDF(s) Uploaded Successfully!")

# --------------- BUTTONS (CENTER-ALIGNED) --------------- #
st.markdown("<div class='center-content'>", unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3, col_btn4 = st.columns([1, 1, 1, 1], gap="small")

with col_btn1:
    submit1 = st.button("📄 Resume Analysis")
with col_btn2:
    submit2 = st.button("✅ Recruitable or Not")
with col_btn3:
    submit3 = st.button("📊 Percentage Match")
with col_btn4:
    submit4 = st.button("🌟 Quality ")

st.markdown("</div>", unsafe_allow_html=True)

# Prompts
input_prompt1 = """
You are an experienced HR with  expertise in computer science ,meachnical ,civil ,electronics and telecommunication,
electical . Review  job description and each resume against the job description.
Highlight strengths and weaknesses based on jobdescription to select a paticular engineering stream relative to the job and resume.
"""

input_prompt3 = """
You are an ATS scanner with expertise . Evaluate  job description and each resume
against the job description, provide a percentage match, list missing keywords,
and share your thoughts,.
"""

input_prompt2 = """
You are an expert  ATS scanner .
Analyze  job description each resume and determine if the applicant is a 'Strong Fit' or 'Not a Fit' depending on job description  .
just tell fit or not 
,dont give extra output.if job description is not provided, remind to provide , for better result
"""

input_prompt4 =""" You are  an expert in English and formats for resume .
your job is to analyze the clarity ,formatting, spelling mistake and grammar in the resume ,
give explaination for each clarity,formatting ,spelling mistake and grammar.
keep proper spacing between lines for each paragraph.
."""

# Processing Resumes
if uploaded_files:
    for uploaded_file in uploaded_files:
        pdf_content = input_pdf_setup(uploaded_file)
        
        if submit1:
            response = get_gemini_response(input_prompt1, pdf_content, input_text)
            st.subheader(f"📄 Analysis for {uploaded_file.name}")
            st.write(response)
        
        if submit3:
            response = get_gemini_response(input_prompt3, pdf_content, input_text)
            st.subheader(f"📊 Percentage Match for {uploaded_file.name}")
            st.write(response)
        
        if submit2:
            response = get_gemini_response(input_prompt2, pdf_content, input_text)
            st.subheader(f"✅ Recruitability for {uploaded_file.name}")
            st.write(response)

        if submit4:
            response = get_gemini_response(input_prompt4, pdf_content, input_text)
            st.subheader(f"✅ Quality for {uploaded_file.name}")
            st.write(response)
