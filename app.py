import streamlit as st
import pdfplumber
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Resume ATS Checker", page_icon="📄", layout="centered")

st.title("📄 Resume ATS Checker")
st.subheader("By Gajanan Pawar")
st.write("Check how well your resume matches a Job Description.")

def extract_text(file):
    try:
        if file.name.endswith('.pdf'):
            with pdfplumber.open(file) as pdf:
                return "".join([p.extract_text() or "" for p in pdf.pages])
        elif file.name.endswith('.docx'):
            doc = docx.Document(file)
            return "\n".join([p.text for p in doc.paragraphs])
        else:
            return file.read().decode('utf-8', errors='ignore')
    except:
        return ""

st.divider()
col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader("Upload Your Resume", type=['pdf','docx','txt'])

with col2:
    jd_text = st.text_area("Paste Job Description", height=200, placeholder="Paste the JD here...")

if st.button("Check ATS Score", type="primary", use_container_width=True):
    if resume_file and jd_text:
        with st.spinner("Analyzing your resume..."):
            resume_text = extract_text(resume_file)
            if not resume_text.strip():
                st.error("Could not extract text from your resume. Please try another file.")
            else:
                vectorizer = TfidfVectorizer().fit_transform([resume_text, jd_text])
                score = cosine_similarity(vectorizer[0:1], vectorizer[1:2])[0][0] * 100

                st.divider()
                st.metric(label="Your ATS Match Score", value=f"{score:.2f}%")
                st.progress(int(score))

                if score > 75:
                    st.success("Excellent Match! ✅ Your resume is highly relevant to this job.")
                elif score > 50:
                    st.warning("Good Match! ⚠️ Consider adding more relevant keywords from the JD.")
                else:
                    st.error("Low Match! ❌ Your resume needs more alignment with the job description.")
    else:
        st.error("Please upload your resume and paste the job description.")
