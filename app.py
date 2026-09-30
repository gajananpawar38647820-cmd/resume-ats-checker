import streamlit as st
import pdfplumber
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Resume ATS Checker")
st.title("📄 Resume ATS Checker - By Gajanan")

def extract_text(file):
    if file.name.endswith('.pdf'):
        with pdfplumber.open(file) as pdf:
            return "".join([p.extract_text() or "" for p in pdf.pages])
    elif file.name.endswith('.docx'):
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        return file.read().decode('utf-8', errors='ignore')

resume_file = st.file_uploader("1. Resume Upload Kara", type=['pdf','docx','txt'])
jd_text = st.text_area("2. Job Description Paste Kara")

if st.button("Check ATS Score"):
    if resume_file and jd_text:
        resume_text = extract_text(resume_file)
        vectorizer = TfidfVectorizer().fit_transform([resume_text, jd_text])
        score = cosine_similarity(vectorizer[0:1], vectorizer[1:2])[0][0] * 100
        st.metric("Tumcha ATS Score", f"{score:.2f}%")
        st.progress(int(score))
        if score > 75:
            st.success("Bhari Resume! ✅")
        else:
            st.warning("Improve kara ⚠️")
    else:
        st.error("Donhi taka!")
