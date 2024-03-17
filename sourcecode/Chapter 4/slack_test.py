import requests
import json

# 슬랙 Incoming Webhook URL
webhook_url = '여기에_당신의_웹후크_URL을_입력하세요'

# 보낼 메시지
message = "Hello, Slack!"
data = {'text': message}

# POST 요청
response = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

# 응답 확인
if response.status_code == 200:
    print("Message sent to Slack")
else:
    print("Failed to send message to Slack")