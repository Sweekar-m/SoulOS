import requests
import json
import re
from LLM_clusters.create_tool_router import sub_create_router

import os
from dotenv import load_dotenv

load_dotenv()  # loads .env automatically

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "mistralai/mistral-7b-instruct-v0.1"

def clean_and_parse_json(raw):
    try:
        # Extract the last valid JSON block
        match = re.findall(r'\{[\s\S]*?\}', raw)
        if match:
            clean = match[-1]
            clean = clean.replace("\\_", "_")
            return json.loads(clean)
    except Exception as e:
        print("⚠️ Failed to parse cleaned JSON:", e)
    print("⚠️ Failed to decode JSON, raw content:\n", raw)
    return {
        "intents": "unknown",
        "response": "I'm not sure what you'd like to create. Please rephrase using 'create' or 'generate'."
    }

def create_ops(prompt: str) -> dict:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    system_prompt = """
You are a precise assistant that reads user prompts and returns the correct intent in strict JSON format.

Your task:

Identify if the user wants to create a file or a presentation.

Return a clean JSON object using one of the defined intents.

If the input does not contain the exact trigger words, return unknown_intent.

Intent Definitions:

create_file
Trigger only if the user explicitly uses "create", "generate", or "make" followed by a known file type: py, html, cpp, js, java, txt.
Expected Output:
{
"intents": "create_file",
"file_type": "<py|html|cpp|js|java|txt>",
"file_name": "<logical_name>.<ext>",
"topic": "<user_input>",
"response": "Creating <file_type> file named <file_name>"
}

create_ppt
Trigger only if the user uses "create", "generate", or "make" along with "PowerPoint" or "presentation".
Expected Output:
{
"intents": "create_ppt",
"file_type": "pptx",
"file_name": "<topic>.pptx",
"topic": "<user_input>",
"page_count": 5,
"save_path": "Documents",
"response": "Creating a PowerPoint on '<topic>' with 5 slides"
}

unknown_intent
Use this when no trigger word is found or the input is ambiguous.
Expected Output:
{
"intents": "unknown_intent",
"response": "I'm not sure what you'd like to create. Please rephrase using 'create' or 'generate'."
}

Rules:

Return only one intent per prompt.

Do not guess. Trigger words must be explicitly present.

Always return valid raw JSON only.

No markdown. No comments. No explanations.

Your goal: zero hallucination and perfectly accurate classification

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
        raw = res.json()["choices"][0]["message"]["content"]
        parsed = clean_and_parse_json(raw)

        sub_create_router(parsed)
        return parsed

    except requests.exceptions.RequestException as e:
        print("❌ API error:", e)
        return {
            "intents": "unknown",
            "response": "LLM API failed. Please try again."
        }
