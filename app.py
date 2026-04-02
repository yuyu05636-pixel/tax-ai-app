import streamlit as st
from PIL import Image
import google.generativeai as genai

# APIキー設定
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# モデル
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("記帳AIアシスタント")

# ① 先にアップローダー
uploaded_file = st.file_uploader("領収書アップロード", type=["png","jpg","jpeg"])

# ② その後にif
if uploaded_file:
    image = Image.open(uploaded_file)

    st.image(image)

    if st.button("仕訳生成"):
        response = model.generate_content([
            "この領収書から仕訳を作成してください。形式：日付,借方,貸方,金額,摘要",
            image
        ])

        st.write(response.text)
