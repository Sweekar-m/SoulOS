import sys
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
from concurrent.futures import ThreadPoolExecutor
from LLM_clusters.create_ops import create_ops  
from LLM_clusters.system_ops import system_ops
def getprompt(text):
    run_all_llms(text)
def run_all_llms(prompt):
    with ThreadPoolExecutor() as executor:
        futures = {
            "system": executor.submit(system_ops, prompt),
            "create": executor.submit(create_ops, prompt),
        }
        resu={k: f.result() for k, f in futures.items()}
    print(resu)
