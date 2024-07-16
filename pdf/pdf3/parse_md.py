import json
import boto3

# プロンプト
prompt = "エネルギー源別最終エネルギー消費について2022年の列のみを抜き出してHTML形式の表(border=1)を出力してください。▲の意味はマイナスです。documentのタグ内の属性情報がある場合は全て削除してください。回答は<html><body><table>で開始してください。文字コードはutf-8を指定してください。縦軸は最終エネルギー消費を含むエネルギー種別、横軸は年度のエネルギー消費・前年度比(%)・シェア(%)にしてください。列の意味を示す行を設けてください。単位は各項目に付与してください。<tr>と</tr>は同じ行に出力してください"

with open("document.md", "r", encoding="utf-8") as file:
    md = file.read()

system_prompt="documentの中にはPDFから抽出したMarkdownが格納されています。質問に回答してください。<document>" + md + "</document>"

content = {"type": "text", "text": prompt}
bedrock = boto3.client('bedrock-runtime')
body = json.dumps(
    {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4000,
        "temperature": 0.0,
        "system": system_prompt,
        "messages": [{"role": "user", "content": [content]}]
    }   
)
response = bedrock.invoke_model(body=body, modelId='anthropic.claude-3-sonnet-20240229-v1:0')
response_body = json.loads(response.get('body').read())
answer = response_body["content"][0]["text"]
print(answer)
