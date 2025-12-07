import os
import subprocess
from google import genai
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Removes ```html, ```css, ```js, and all backticks completely
def clean_output(text):
    import re
    text = re.sub(r"```.*?\n", "", text)  # remove ```html, ```css etc
    text = text.replace("```", "")
    return text.strip()


def vibe_code(prompt):
    client = genai.Client()

    # SYSTEM PROMPT for planning
    system_plan = (
        "You are a strict code generator. "
        "Output ONLY pure JSON with no markdown, no backticks, no explanations. "
        "Never add ``` or language descriptions. "
        "Only return valid JSON."
    )

    plan_prompt = (
        f"{system_plan}\n"
        f"User request: \"{prompt}\"\n\n"
        "{\n"
        "  \"project_name\": \"folder_name\",\n"
        "  \"files\": {\n"
        "    \"index.html\": \"main page\",\n"
        "    \"style.css\": \"styling\",\n"
        "    \"script.js\": \"javascript logic\"\n"
        "  }\n"
        "}"
    )

    plan_resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=plan_prompt
    )

    # Extract pure JSON
    import re, json
    match = re.search(r"\{[\s\S]*\}", plan_resp.text)
    if not match:
        print("Invalid JSON output:\n", plan_resp.text)
        return

    plan = json.loads(match.group())

    project_name = plan["project_name"].replace(" ", "_")
    files = plan["files"]

    base = r"D:\vibe_projects"
    project_path = os.path.join(base, project_name)

    # Create project folder
    os.makedirs(project_path, exist_ok=True)

    # Create images folder also (just in case)
    os.makedirs(os.path.join(project_path, "images"), exist_ok=True)

    # Generate all files
    for file_name, desc in files.items():

        system_code = (
            "You are a strict code generator. "
            "Output ONLY pure code with zero markdown, zero backticks, zero comments, zero explanations. "
            "Never use ``` or language tags. Only raw code."
        )

        code_prompt = (
            f"{system_code}\n\n"
            f"Generate the full code for '{file_name}'.\n"
            f"Project request: \"{prompt}\"\n"
            f"Description: {desc}\n\n"
            "If images are needed, use ONLINE image URLs only."
        )

        code_resp = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=code_prompt
        )

        content = clean_output(code_resp.text)

        # Save created file
        file_path = os.path.join(project_path, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        print("Created →", file_path)

    # Open project in VS Code
    try:
        vscode = r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe"
        subprocess.Popen([vscode, project_path])
    except:
        os.startfile(project_path)

    print("\n🔥 Project Ready in VS Code!")
    return project_path


# Test

