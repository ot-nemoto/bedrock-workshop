from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
import streamlit as st

# モデル選択
use_model = st.sidebar.selectbox("使用するモデルを選択してください",("Sonnet","Haiku"))

# 初回はsession領域を作成
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 2回目以降はsessionを元に全量再描画を行う        
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 入力された場合
if user_prompt := st.chat_input():
    
    # モデルの決定
    if use_model == "Sonnet":
        modelId = "anthropic.claude-3-sonnet-20240229-v1:0"
    elif use_model == "Haiku":
        modelId = "anthropic.claude-3-haiku-20240307-v1:0"

    # chainの定義
    prompt = ChatPromptTemplate.from_messages([
        ("system","あなたはAIチャットボットです"),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="human_message")])
    LLM = ChatBedrock(model_id=modelId, model_kwargs={"max_tokens": 4000})
    chain = prompt | LLM

    # 入力内容の描画
    with st.chat_message("user"):
        st.write(user_prompt)
    # chainをstreamで実行し生成内容をstreamで出力
    with st.chat_message("assistant"):
        response = st.write_stream(chain.stream({"messages": st.session_state.messages, "human_message": [HumanMessage(content=user_prompt)]}))

    # 入力内容と生成内容をsession領域に格納
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.session_state.messages.append({"role": "assistant", "content": response})
