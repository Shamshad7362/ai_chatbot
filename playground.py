import requests
import json
from backend.config import OPEN_ROUTERAI_API_KEY
from backend.ai_service import Chatbot

MODEL = "apodex/apodex-1.1-mini:free"

bot = Chatbot(OPEN_ROUTERAI_API_KEY)
bot.model = MODEL

# for chunk in bot.ask_stream("Explain AI in simple words"):
#     print(chunk, end="", flush=True)

full_msg=bot.ask("Explain AI in simple words")
print(full_msg)

# response = requests.post(
#     "https://openrouter.ai/api/v1/chat/completions",
#     headers={
#         "Authorization": f"Bearer {OPEN_ROUTERAI_API_KEY}",
#         "Content-Type": "application/json",
#     },
#     json={
#         "model": MODEL,
#         "stream":True,
#         "messages": [{"role": "user", "content": "Hello"}],
#         "reasoning": {"enabled": True},
#     },
#     stream=True,
#     timeout=60,
# )
#
# print(f"HTTP status: {response.status_code}")
# response.raise_for_status()
#
# print("\nRaw stream events:")
#
#
# for raw_line in response.iter_lines():
#     if not raw_line:
#         continue
#
#     line = raw_line.decode("utf-8") if isinstance(raw_line, bytes) else raw_line
#
#     if not line.startswith("data: "):
#         continue
#
#     data = line[len("data: "):]
#
#     if data == "[DONE]":
#         print("\nStream finished.")
#         break
#
#     event = json.loads(data)
#     delta = event["choices"][0]["delta"]
#
#     # Print only the answer text, piece by piece.
#     chunk = delta.get("content", "")
#     if chunk:
#         print(chunk, end="", flush=True)
