import streamlit as st
import PyPDF2

st.title("Resume ATS Checker")

uploaded_file = st.file_uploader("Upload resume (upto 5MB)", type="pdf")
job_desc = st.text_area("Paste Job Description")

if st.button("Check ATS Score"):
    if uploaded_file:
        # 5MB limit
        if uploaded_file.size > 5 * 1024 * 1024:
            st.error("File motha aahe, 5MB peksha lahan tak")
        else:
            reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for p in reader.pages:
                text += p.extract_text() or ""
            st.success(f"Size: {uploaded_file.size/1024:.0f} KB - Upload zala!")
            st.write(f"Matched ani Missing keywords khali yetil...")
            # yethun pudhe score logic
            jd_words = set(job_desc.lower().split())
            res_words = set(text.lower().split())
            score = len(jd_words & res_words) / len(jd_words) * 100 if jd_words else 0
            st.metric("ATS Score", f"{score:.1f}%")
            st.write("Missing:", list(jd_words - res_words)[:10])
