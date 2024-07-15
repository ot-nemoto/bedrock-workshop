import streamlit as st
import boto3

st.title("Knowledge base RAGアプリケーションサンプル２")
use_model = st.selectbox("使用するモデルを選択してください",("Sonnet","Haiku"))
user_input = st.text_input("質問")
send_button = st.button("送信")

if send_button and user_input:

    if use_model == "Sonnet":
        modelId = "anthropic.claude-3-sonnet-20240229-v1:0"
    elif use_model == "Haiku":
        modelId = "anthropic.claude-3-haiku-20240307-v1:0"

    knowledgebase = boto3.client("bedrock-agent-runtime")
    response = knowledgebase.retrieve_and_generate(
        input={"text": user_input},
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "generationConfiguration": {
                    "promptTemplate": {
                        "textPromptTemplate": "あなたはdocumentsを参考に質問に回答します。<documents>$search_results$</documents>\ndocumentsを参考にせずに回答する場合は、「資料にありませんが、私の知識では」と言う言葉の後に、知識で回答します。"
                    },
                },
                "knowledgeBaseId": "4NMVQBZW3G",
                "modelArn": "arn:aws:bedrock:us-west-2::foundation-model/"+modelId,
                "retrievalConfiguration": { 
                    "vectorSearchConfiguration": { 
                        "numberOfResults": 30,
                        "overrideSearchType": "HYBRID"
                    },
                },
            },
        },
    )
    st.write(response["output"]["text"])
