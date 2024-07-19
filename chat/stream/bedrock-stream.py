import json

import boto3

bedrock = boto3.client(service_name="bedrock-runtime")

body = json.dumps(
    {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4000,
        "messages": [{"role": "user", "content": "カレーの作り方を説明してください"}],
    }
)

response = bedrock.invoke_model_with_response_stream(
    modelId="anthropic.claude-3-haiku-20240307-v1:0", body=body
)

stream = response.get("body")
if stream:
    for event in stream:
        chunk = event.get("chunk")
        if chunk:
            chunk_json = json.loads(chunk.get("bytes").decode())
            if chunk_json["type"] == "content_block_delta":
                print(chunk_json["delta"]["text"], end="", flush=True)
