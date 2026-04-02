import streamlit as st
from PIL import Image
import google.generativeai as genai
import io

# APIキー
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash-latest")
st.title("記帳AIアシスタント")

uploaded_file = st.file_uploader("領収書アップロード", type=["png","jpg","jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image)

    if st.button("仕訳生成"):
        with st.spinner("処理中..."):

            try:
                # ここが重要（変換）
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format="JPEG")
                img_bytes = img_byte_arr.getvalue()

                response = model.generate_content([
                    "この領収書から仕訳を作成してください。形式：日付,借方,貸方,金額,摘要",
                    {
                        "mime_type": "image/jpeg",
                        "data": img_bytes
                    }
                ])

                st.success("完了！")
                st.write(response.text)

            except Exception as e:
                st.error(f"エラー: {e}")
