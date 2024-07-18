import json

import boto3

#モデルの設定
#modelId="anthropic.claude-3-sonnet-20240229-v1:0"
modelId="anthropic.claude-3-haiku-20240307-v1:0"

#プロンプトの設定
user_prompt = "カレーの作り方を説明してください"

bedrock = boto3.client('bedrock-runtime')
body = json.dumps(
    {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4000,
        "messages": [{"role": "user","content": user_prompt}]
    }
)

# Bedrockの呼び出し
response = bedrock.invoke_model(body=body,modelId=modelId)

# Bedrock呼出し結果の抽出
response_body = json.loads(response.get('body').read())
answer = response_body["content"][0]["text"]

# 結果の出力
print(answer)