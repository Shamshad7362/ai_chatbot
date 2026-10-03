import requests
import json
import markdown

class Chatbot:
    def __init__(self,api_key,model="inclusionai/ling-3.0-flash-vl:free"):
        self.api_key = api_key
        self.model = model
        self.messages = []
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    def ask(self, question):
        self.messages.append({"role": "user", "content": question})
        response = requests.post(
            url=self.url,
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

    def ask_stream(self, question):
        self.messages.append({"role": "user", "content": question})
        answer_parts = []

        with requests.post(
                url=self.url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "stream": True,
                    "messages": self.messages,
                },
                stream=True,
                timeout=60,
        ) as response:
            response.raise_for_status()

            for line in response.iter_lines():
                if not line or not line.startswith(b"data: "):
                    continue

                data = line[len(b"data: "):]

                if data == b"[DONE]":
                    break

                event = json.loads(data)
                choices = event.get("choices", [])
                if not choices:
                    continue

                chunk = choices[0].get("delta", {}).get("content", "")
                if chunk:
                    answer_parts.append(chunk)
                    yield chunk

        # Save the finished assistant reply for the next turn.
        self.messages.append({
            "role": "assistant",
            "content": "".join(answer_parts),
        })

















