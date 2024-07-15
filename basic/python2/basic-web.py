import boto3
import json
import streamlit as st

# Web I/Fの追加
st.title("Claude3を触ってみよう")
use_model = st.selectbox("使用するモデルを選択してください",("Sonnet","Haiku"))
system_prompt = st.text_area("システムプロンプト","あなたは質問に回答するAIアシスタントです")
user_prompt = st.text_area("ユーザープロンプト")
send_button = st.button("送信")

# 送信ボタンを押下
if send_button and system_prompt and user_prompt:

    if use_model == "Sonnet":
        modelId = "anthropic.claude-3-sonnet-20240229-v1:0"
    elif use_model == "Haiku":
        modelId = "anthropic.claude-3-haiku-20240307-v1:0"

    bedrock = boto3.client('bedrock-runtime')
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4000,
            "system": system_prompt,
            "messages": [{"role": "user","content": user_prompt}]
        }
    )
    
    # Bedrockの呼び出し
    response = bedrock.invoke_model(body=body,modelId=modelId)
    
    # Bedrock呼出し結果の抽出
    response_body = json.loads(response.get('body').read())
    answer = response_body["content"][0]["text"]

    # 結果の出力
    st.write(answer)
