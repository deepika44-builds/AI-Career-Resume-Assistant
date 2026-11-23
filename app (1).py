
import streamlit as st
import os
import io
from google import genai
from pypdf import PdfReader

st.set_page_config(
    page_title="AI Career & Resume Assistant",
    page_icon="💼",
    layout="wide"
)

st.title("💼 AI Career & Resume Assistant")
st.write("Your AI-powered career development companion.")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key not found. Configure GEMINI_API_KEY before starting the app.")
    st.stop()

client = genai.Client(api_key=api_key)

@st.cache_data
def extract_resume(pdf_bytes):
    pdf = PdfReader(io.BytesIO(pdf_bytes))
    return "\n".join(page.extract_text() or "" for page in pdf.pages)

st.sidebar.header("Navigation")

feature = st.sidebar.radio(
    "Choose a feature",
    [
        "Resume Analyzer",
        "Job Description Matcher",
        "Skill Gap Analyzer",
        "Interview Preparation"
    ]
)

st.sidebar.success("AI Career Assistant is ready!")

uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)

resume_text = ""

if uploaded_file:
    try:
        resume_text = extract_resume(uploaded_file.getvalue())
        if resume_text.strip():
            st.success("Resume uploaded successfully!")
        else:
            st.warning("No readable text found in this PDF.")
    except Exception as e:
        st.error(f"Could not read PDF: {e}")

def ask_gemini(prompt):
    try:
        with st.spinner("AI is analysing..."):
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )
        return response.text
    except Exception as e:
        return f"Gemini request failed: {e}"

if feature == "Resume Analyzer":
    st.header("📄 Resume Analyzer")
    st.write("Get feedback and suggestions to improve your resume.")

    if st.button("Analyse Resume"):
        if not resume_text.strip():
            st.warning("Please upload a readable PDF resume first.")
        else:
            prompt = f"""
            Analyse this student resume.

            Give:
            1. Overall feedback
            2. Strengths
            3. Technical skills
            4. Missing skills
            5. Improvement suggestions
            6. Suitable internships and entry-level jobs
            7. Resume score out of 10 with reasons

            Never invent qualifications or experience.

            RESUME:
            {resume_text[:12000]}
            """
            st.markdown(ask_gemini(prompt))

elif feature == "Job Description Matcher":
    st.header("🎯 Job Description Matcher")

    job_description = st.text_area(
        "Paste the job description",
        height=220
    )

    if st.button("Match Resume"):
        if not resume_text.strip():
            st.warning("Upload your resume first.")
        elif not job_description.strip():
            st.warning("Enter a job description.")
        else:
            prompt = f"""
            Compare this resume with the job description.

            RESUME:
            {resume_text[:10000]}

            JOB DESCRIPTION:
            {job_description[:8000]}

            Provide:
            1. Match score out of 100
            2. Matching skills
            3. Missing skills
            4. Strengths
            5. Suggestions for improvement

            Do not invent skills or experience.
            """
            st.markdown(ask_gemini(prompt))

elif feature == "Skill Gap Analyzer":
    st.header("📚 Skill Gap Analyzer")

    target_role = st.text_input(
        "Enter your target career role",
        placeholder="Example: Python Developer"
    )

    if st.button("Analyse Skill Gaps"):
        if not resume_text.strip():
            st.warning("Upload your resume first.")
        elif not target_role.strip():
            st.warning("Enter a target role.")
        else:
            prompt = f"""
            Analyse this resume for the role: {target_role}

            RESUME:
            {resume_text[:10000]}

            Provide:
            1. Existing skills
            2. Missing skills
            3. Beginner-friendly learning roadmap
            4. Three project ideas
            5. Recommended technologies
            6. A realistic 30-day learning plan

            Do not claim the student has skills not shown in the resume.
            """
            st.markdown(ask_gemini(prompt))

elif feature == "Interview Preparation":
    st.header("🎤 Interview Preparation")
    st.write("Practise technical and HR questions.")

    target_role = st.text_input(
        "Enter the job role",
        placeholder="Example: Python Developer"
    )

    if st.button("Generate Interview Questions"):
        if not target_role.strip():
            st.warning("Enter a job role.")
        else:
            role = target_role.lower()

            if "python" in role:
                questions = [
                    "What are Python's main features?",
                    "What is the difference between a list and a tuple?",
                    "What are functions?",
                    "Explain loops in Python.",
                    "What is exception handling?",
                    "What is object-oriented programming?",
                    "What are Python dictionaries?",
                    "What is the __init__ method?"
                ]
            elif "data" in role or "machine learning" in role:
                questions = [
                    "What is data analysis?",
                    "What is NumPy?",
                    "What is Pandas?",
                    "What is data cleaning?",
                    "What is supervised learning?",
                    "What is unsupervised learning?",
                    "What is overfitting?",
                    "What is a classification model?"
                ]
            else:
                questions = [
                    "What is a data structure?",
                    "What is an algorithm?",
                    "What is version control?",
                    "What is GitHub?",
                    "What is debugging?",
                    "What is an API?",
                    "What is database management?",
                    "What is software testing?"
                ]

            st.subheader("Technical Questions")
            for i, question in enumerate(questions, 1):
                st.write(f"**{i}.** {question}")

            st.subheader("HR Questions")
            hr_questions = [
                "Tell me about yourself.",
                "Why are you interested in this role?",
                "What are your strengths?",
                "Describe a project you have completed.",
                "How do you handle learning something new?"
            ]

            for i, question in enumerate(hr_questions, 1):
                st.write(f"**{i}.** {question}")

            st.subheader("Project-Based Questions")
            project_questions = [
                "Explain your project and its objective.",
                "Which technologies did you use and why?",
                "What challenges did you face?"
            ]

            for i, question in enumerate(project_questions, 1):
                st.write(f"**{i}.** {question}")

st.divider()
st.caption("AI Career & Resume Assistant | Built with Python, Streamlit and Google Gemini API")
