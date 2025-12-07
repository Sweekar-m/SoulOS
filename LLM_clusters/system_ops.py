import requests
import json
import re
from LLM_clusters.system_tool_router import sub_system_router
import os
from dotenv import load_dotenv

load_dotenv()  # loads .env automatically   
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "mistralai/mistral-7b-instruct-v0.1"

def extract_json(text):
    try:
        # Find all valid JSON-looking blocks
        matches = re.findall(r'\{[\s\S]*?\}', text)

        # Try parsing each one, pick the first valid JSON
        for match in reversed(matches):
            cleaned = match.replace('\\_', '_')  # Fix invalid escapes
            try:
                return json.loads(cleaned)
            except:
                continue
        raise ValueError("No valid JSON found")
    except Exception as e:
        print("⚠️ Failed to parse LLM output:", e)
        print("Raw content was:\n", text)
        return None


def system_ops(prompt: str) -> dict:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    system_prompt = """
You are a strict intent classifier. Read `user_input` and return exactly **one intent** as JSON.

Rules:
1. Match only exact trigger words; do NOT guess.
2. If no triggers match 100%, return "unknown_intent".
3. Always return a JSON object, no extra text.

Intents:

1. open_application
Trigger: "open", "launch", "start"
- Only match if input starts/includes trigger word and no "create", "make", "generate".
- Extract app_name, target (contact/file/field), action (type/send_message/click), content (text/code/message)
JSON:
{
  "intents": "open_application",
  "app_name": "<name after trigger>",
  "action": "True|False",
  "action_type": "<type/send_message/click or None>",
  "target": "<contact, file, field or None>",
  "content": "<text/code/message or None>",
  "response": "✅ Opened <app_name> and ready for action"
}

2. open_qr
Trigger: "QR", "QR code", "show QR", "display QR"
JSON:
{
  "intents": "open_qr",
  "response": "<pc: 'Here's your QR code' | web: 'Pulled it up!'>"
}

3. web_search
Trigger: "search", "look up", "find"
JSON:
{
  "intents": "web_search",
  "user_input": "<original input>",
  "query": "<trimmed query after trigger>",
  "num_results": 1,
  "response": "<pc: direct reply | web: 'Searching the web for you'>"
}

Default:
{
  "intents": "unknown_intent",
  "response": "Sorry, I couldn't detect a clear action. Please rephrase."
}


"""

    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": prompt.strip()}
        ]
    }

    try:
        res = requests.post(url, headers=headers, json=body)
        res.raise_for_status()
        raw_content = res.json()["choices"][0]["message"]["content"]
        parsed = extract_json(raw_content)

        if parsed:
            sub_system_router(parsed)
            return parsed
        else:
            return {"error": "❌ Invalid LLM JSON format."}

    except requests.exceptions.RequestException as e:
        print("❌ API request failed:", e)
        return {"error": "API request failed"}
    except Exception as e:
        print("❌ Unexpected error:", e)
        return {"error": "Unexpected error"}
