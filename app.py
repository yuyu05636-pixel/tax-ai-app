response = client.responses.create(
    model="gpt-4.1-mini",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": """
領収書から仕訳を作成してください

形式：
日付,借方科目,貸方科目,金額,摘要
"""}
                ,
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{image_base64}"
                }
            ]
        }
    ]
)
