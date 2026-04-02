from PIL import Image

if uploaded_file:
    image = Image.open(uploaded_file)  # ←これ追加

    st.image(image)

    if st.button("仕訳生成"):
        response = model.generate_content([
            "この領収書から仕訳を作成してください。形式：日付,借方,貸方,金額,摘要",
            image   # ←ここを変更
        ])

        st.write(response.text)
