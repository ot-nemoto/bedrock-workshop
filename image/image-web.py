import base64
import copy
import json

import boto3
import numpy as np
import streamlit as st
from PIL import Image

st.title("画像解析Webアプリケーション")
use_model = st.selectbox("使用するモデルを選択してください", ("Sonnet", "Haiku"))
img_file = st.file_uploader("Jpegファイルアップロード", type=["jpeg"])
thumbnail_space = st.empty()  # サムネイル表示用の欄を作っておく
input_text = st.text_area("画像に対して質問してください")
send_button = st.button("送信")

if img_file:  # 画像がアップロードされている場合
    img_file_copy = copy.copy(img_file)  # コピーしてからサムネイル表示
    image = Image.open(img_file_copy)
    img_array = np.array(image)
    thumbnail_space.image(img_array, width=200)

# 送信ボタン押下
if send_button and input_text:
    if use_model == "Sonnet":
        modelId = "anthropic.claude-3-sonnet-20240229-v1:0"
    elif use_model == "Haiku":
        modelId = "anthropic.claude-3-haiku-20240307-v1:0"

    # content配列の初期化
    content = []

    if img_file:  # 画像がアップロードされている場合
        image = img_file.read()  # 読み込み
        b64 = base64.b64encode(image).decode("utf-8")  # Base64変換

        # プロンプトの形式にしてcontent配列に追加
        content_image = {
            "type": "image",
            "source": {"type": "base64", "media_type": "image/jpeg", "data": b64},
        }
        content.append(content_image)

    # 入力テキストをcontent配列に追加
    content_text = {"type": "text", "text": input_text}
    content.append(content_text)

    bedrock = boto3.client("bedrock-runtime")
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4000,
            "messages": [{"role": "user", "content": content}],
        }
    )
    response = bedrock.invoke_model(body=body, modelId=modelId)
    response_body = json.loads(response.get("body").read())
    answer = response_body["content"][0]["text"]
    st.code(answer)
