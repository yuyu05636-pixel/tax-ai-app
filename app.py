import streamlit as st
import pandas as pd
from PIL import Image
import base64
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("記帳AIアシスタント")

uploaded_file = st.file_uploader("領収書をアップロード", type=["png", "jpg", "jpeg"])

def encode_image(file):
    return base64.b64encode(file.read()).decode("utf-8")

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image)

    if st.button("仕訳生成"):

        img_base64 = encode_image(uploaded_file)

        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "あなたは税理士です"},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": """
領収書から仕訳を作成してください

形式：
日付,借方科目,貸方科目,金額,摘要
"""}
                        ,
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_base64}"
                            }
                        }
                    ]
                }
            ]
        )

        result = response.choices[0].message.content

        st.write(result)

        df = pd.DataFrame([result], columns=["仕訳"])
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button("CSVダウンロード", csv, "journal.csv")
