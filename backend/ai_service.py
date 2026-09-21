import requests
import json


class Chatbot:
    def __init__(self,api_key,model="inclusionai/ling-3.0-flash-vl:free"):
        self.api_key = api_key
        self.model = model
        self.messages = []

    def ask(self, question):
        self.messages.append({"role": "user", "content": question})
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": self.model,
                "messages": self.messages,
                "reasoning": {"enabled": True}
            })
        )
        print(f"response is {response.status_code}")
        response = response.json()
        assistant_message = response['choices'][0]['message']
        self.messages.append({
            "role": "assistant",
            "content": assistant_message.get('content'),
            "reasoning_details": assistant_message.get('reasoning_details')
        })
        return assistant_message.get('content')
















