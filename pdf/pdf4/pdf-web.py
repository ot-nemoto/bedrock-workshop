import io
import json

import boto3
import pymupdf4llm
import streamlit as st
from pdfminer.converter import HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pymupdf import Document

st.title("PDF解析アプリケーション")
pdf_file = st.file_uploader("PDFファイルアップロード", type="pdf")
max_pages = st.number_input("解析するページ数", 1, 200, 3)
parse = st.selectbox(
    "変換方法を選択してください", ("Text抽出", "HTML変換", "Markdown変換")
)
use_model = st.selectbox("使用するモデルを選択してください", ("Sonnet", "Haiku"))
input_text = st.text_area("PDFに対する解析指示や質問をしてください")
send_button = st.button("送信")

# 送信ボタン押下
if send_button and input_text and pdf_file:
    text = ""

    if parse == "Text抽出" or parse == "HTML変換":
        resource_manager = PDFResourceManager()
        text_buffer = io.StringIO()

        if parse == "Text抽出":
            converter = TextConverter(
                resource_manager, text_buffer, laparams=LAParams()
            )
        else:
            converter = HTMLConverter(
                resource_manager, text_buffer, laparams=LAParams()
            )

        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        for page in PDFPage.get_pages(
            pdf_file, maxpages=max_pages, check_extractable=False
        ):
            page_interpreter.process_page(page)
            text += text_buffer.getvalue()
            text_buffer.truncate(0)
            text_buffer.seek(0)
        converter.close()
        text_buffer.close()
    else:
        text = pymupdf4llm.to_markdown(
            Document(stream=pdf_file.getvalue()),
            pages=range(0, max_pages),
            margins=(0, 0, 0, 0),
        )

    # プロンプトの組み立て、LLMの実行
    if use_model == "Sonnet":
        modelId = "anthropic.claude-3-sonnet-20240229-v1:0"
    elif use_model == "Haiku":
        modelId = "anthropic.claude-3-haiku-20240307-v1:0"

    system_prompt = (
        "documentの中にはPDFから抽出したテキストが格納されています。質問に回答してください。<document>"
        + text
        + "</document>"
    )
    content = {"type": "text", "text": input_text}
    bedrock = boto3.client("bedrock-runtime")
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4000,
            "temperature": 0.0,
            "system": system_prompt,
            "messages": [{"role": "user", "content": [content]}],
        }
    )
    response = bedrock.invoke_model(body=body, modelId=modelId)
    response_body = json.loads(response.get("body").read())
    answer = response_body["content"][0]["text"]

    st.code(answer)
