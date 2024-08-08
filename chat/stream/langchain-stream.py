import streamlit as st
from langchain_aws import ChatBedrock

# chainの定義
LLM = ChatBedrock(
    model_id="anthropic.claude-3-haiku-20240307-v1:0", model_kwargs={"max_tokens": 4000}
)
chain = LLM

## ストリーミングで実行
for chunk in chain.stream("カレーの作り方を説明してください"):
    print(chunk.content, end="", flush=True)
