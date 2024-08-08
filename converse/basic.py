import boto3

# モデルの設定
# modelId="anthropic.claude-3-sonnet-20240229-v1:0"
modelId = "anthropic.claude-3-haiku-20240307-v1:0"

# プロンプトの設定
user_prompt = "カレーの作り方を説明してください"

bedrock = boto3.client("bedrock-runtime")
messages = [{"role": "user", "content": [{"text": user_prompt}]}]
inferenceConfig = {"maxTokens": 4000}

# Bedrockの呼び出し
response = bedrock.converse(
    modelId=modelId, messages=messages, inferenceConfig=inferenceConfig
)

# Bedrock呼出し結果の抽出
answer = response["output"]["message"]["content"][0]["text"]

# 結果の出力
print(answer)
