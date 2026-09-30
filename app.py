import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from analyzer import analyze_sentiment

st.set_page_config(page_title="AI Sentiment Analyzer", page_icon="🤖")
st.title("🤖 AI Driven Sentiment Analyzer")
st.write("By Gajanan Pawar | Python Internship Project")

text_input = st.text_area("Yethe tumcha review / comment taka:", "I love this product, amazing quality!")

if st.button("Analyze Sentiment"):
    result = analyze_sentiment(text_input)
    st.success(f"Result: {result['sentiment']}")
    st.write(f"Polarity: {result['polarity']}")
    
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [result['positive_%'], result['negative_%'], result['neutral_%']]
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    st.pyplot(fig)
    st.write(f"Positive: {result['positive_%']}% | Negative: {result['negative_%']}% | Neutral: {result['neutral_%']}%")

st.markdown("---")
st.write("Bulk Check sathi CSV upload kara")
uploaded = st.file_uploader("Upload CSV", type=['csv'])
if uploaded:
    df = pd.read_csv(uploaded)
    df['Sentiment'] = df.iloc[:,0].apply(lambda x: analyze_sentiment(str(x))['sentiment'])
    st.write(df)
