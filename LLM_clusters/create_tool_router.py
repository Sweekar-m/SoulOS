from tools.ppt import ppt_file_fun
from tools.create import vibe_code

def sub_create_router(intent:dict):
    intent_type = intent.get("intents", "")
    print("THE INTENT TYPE IS=",intent_type)
    if intent_type == "create_file":
        file_type = intent.get("file_type", "")
        file_name = intent.get("file_name", "")
        topic = intent.get("topic", "")
        response = intent.get("response", "")
        vibe_code(topic)
    elif intent_type == "create_ppt":
        fileName= intent.get("file_name", "")
        topics = intent.get("topic", "")
        page_count = intent.get("page_count", 5)
        print(fileName)
        print(topics)
        print(page_count)
        ppt_file_fun(fileName,page_count,topics )
    else:
        print(f"Unknown create intent: {intent_type}")