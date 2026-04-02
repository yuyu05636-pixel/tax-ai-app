import streamlit as st
from PIL import Image
from google import genai
import io

# クライアント作成
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.title("記帳AIアシスタント")

uploaded_file = st.file_uploader("領収書アップロード", type=["png","jpg","jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image)

    if st.button("仕訳生成"):
        with st.spinner("処理中..."):
            try:
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format="JPEG")
                img_bytes = img_byte_arr.getvalue()

                response = client.models.generate_content(
                    model="gemini-2.0-flash",  # ←これが正解
                    contents=[
                        "この領収書から仕訳を作成してください。形式：日付,借方,貸方,金額,摘要",
                        {
                            "mime_type": "image/jpeg",
                            "data": img_bytes
                        }
                    ]
                )

                st.success("完了！")
                st.write(response.text)

            except Exception as e:
                st.error(f"エラー: {e}")
