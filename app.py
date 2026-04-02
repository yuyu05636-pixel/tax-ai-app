import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

st.title("記帳AIアシスタント")

uploaded_file = st.file_uploader("領収書アップロード", type=["png","jpg","jpeg"])

if uploaded_file:
    st.image(uploaded_file)

    if st.button("仕訳生成"):
        response = model.generate_content([
            "この領収書から仕訳を作成してください。形式：日付,借方,貸方,金額,摘要",
            uploaded_file
        ])

        st.write(response.text)

