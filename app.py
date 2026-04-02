import streamlit as st
import pandas as pd
import base64
from openai import OpenAI

# APIクライアント
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("記帳AIアシスタント")

uploaded_file = st.file_uploader("領収書アップロード", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file)

    if st.button("仕訳生成"):
        with st.spinner("処理中..."):

            image_bytes = uploaded_file.read()
            image_base64 = base64.b64encode(image_bytes).decode()

            try:
                response = client.responses.create(
                    model="gpt-4.1-mini",
                    input=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "input_text",
                                    "text": """
領収書から仕訳を作成してください

形式：
日付,借方科目,貸方科目,金額,摘要
"""
                                },
                                {
                                    "type": "input_image",
                                    "image_url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            ]
                        }
                    ]
                )

                result = response.output[0].content[0].text

                st.success("完了！")
                st.write(result)

                df = pd.DataFrame([result], columns=["仕訳"])
                csv = df.to_csv(index=False).encode("utf-8")

                st.download_button("CSVダウンロード", csv, "journal.csv")

            except Exception as e:
                st.error(f"エラー: {e}")
