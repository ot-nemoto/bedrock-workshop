from langchain_core.prompts import ChatPromptTemplate
from langchain_aws.chat_models import ChatBedrock
from langchain_aws.retrievers import AmazonKnowledgeBasesRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import streamlit as st

st.title("Knowledge base RAGアプリケーションサンプル")
use_model = st.selectbox("使用するモデルを選択してください",("Sonnet","Haiku"))
user_input = st.text_input("質問")
send_button = st.button("送信")

if send_button and user_input:
    
    if use_model == "Sonnet":
        modelId = "anthropic.claude-3-sonnet-20240229-v1:0"
    elif use_model == "Haiku":
        modelId = "anthropic.claude-3-haiku-20240307-v1:0"

    # promptの定義
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system","""
            あなたはdocumentsを参考に質問に回答します。<documents>{context}</documents>
            documentsを参考にせずに回答する場合は、「資料にありませんが、私の知識では」と言う言葉の後に、知識で回答します。
            """),
            ("human","{question}")
        ]
    )
    
    # LLMの定義
    LLM = ChatBedrock(model_id=modelId, model_kwargs={"temperature": 0, "max_tokens": 4000})
    
    # Retriever(KnowledgeBase)の定義
    # Knowledge base ID、取得件数、検索方法（ハイブリッド）
    retriever = AmazonKnowledgeBasesRetriever(
        knowledge_base_id="4NMVQBZW3G",
        retrieval_config={
            "vectorSearchConfiguration": {
                "numberOfResults": 30, 
                "overrideSearchType": "HYBRID"
            }
        }
    )
    
    # chainの定義
    chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | LLM | StrOutputParser()
    
    # chainの実行
    answer = chain.invoke(user_input)

    # 実行結果の出力
    st.write(answer)
