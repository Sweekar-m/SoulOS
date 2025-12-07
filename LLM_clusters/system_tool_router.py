
import sys
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
from tools.open_app import open_app_fun
from tools.show_qr_tool import show_qr_fun
from tools.search_web import search_and_open


def sub_system_router(intent: dict):
    intent_type = intent.get("intents", "")
    action=str(intent.get("action","none"))
    print(action)
    
    print("INTENTE_TYPE",intent_type)
    if intent_type == "open_application":
        app_name = intent.get("app_name", "")
        response = intent.get("response", "")
        action_type=intent.get("action_type","") 
        print("ACTION TYPE",action_type)
        target=intent.get("target","")
        content=intent.get("content","")
        open_app_fun(app_name)
        
    elif intent_type == "open_qr":
        response = intent.get("response", "")
        result = show_qr_fun()
        
    elif intent_type == "web_search":
        query = intent.get("user_input", "")
        num_results = intent.get("num_results", 1)
        response = intent.get("response", "")
        search_and_open(query,3)
        
    else:
        print(f"Unknown system intent: {intent_type}")