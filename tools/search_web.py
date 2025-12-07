import webbrowser
from ddgs import DDGS
import google.generativeai as genai

# ----------------------------
#  CONFIGURE GEMINI
# ----------------------------
import sys
import os
from dotenv import load_dotenv
load_dotenv()  # loads .env automatically
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY") 
genai.configure()

# Words that force YouTube-only search
YOUTUBE_KEYWORDS = ["youtube", "yt", "video", "song", "music", "mv", "clip","live","videoes"]


# ----------------------------
#  GEMINI → CLEAN QUERY
# ----------------------------
def rewrite_query(query):
    prompt = f"Rewrite this into a clean search engine query and remove all the words like bro buddy or something like that and don't give me any exrtra content just return the query:\n\"{query}\""

    try:
        resp = genai.GenerativeModel("gemini-2.5-flash").generate_content(prompt)
        clean = resp.text.strip()
        return clean if clean else query
    except:
        print("⚠️ Gemini Error → Using raw query.")
        return query


# ----------------------------
#  DIRECT YOUTUBE SEARCH
# ----------------------------
def youtube_search(query):
    yt_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    print("🎥 Opening YouTube Search:", yt_url)
    webbrowser.open(yt_url)


# ----------------------------
#  MAIN SEARCH LOGIC
# ----------------------------
def stable_search(query, num_results=5):
    print(f"🔍 Searching (DuckDuckGo): {query}")

    links = []

    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=num_results, safesearch="off"):
                url = r.get("href", "")
                if url.startswith("http"):
                    links.append(url)
    except Exception as e:
        print("⚠️ DDG Error:", e)

    if not links:
        bing = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
        print("⚠️ DDG empty → Opening Bing")
        webbrowser.open(bing)
        return

    for url in links:
        print("🌐 Opening:", url)
        webbrowser.open(url)


# ----------------------------
#  FINAL COMBINED FUNCTION
# ----------------------------
def search_and_open(query, num_results=5):

    # ---- 1) Check if YouTube-type query ----
    if any(k in query.lower() for k in YOUTUBE_KEYWORDS):
        clean_query = rewrite_query(query)
        youtube_search(clean_query)
        return

    # ---- 2) Otherwise normal search ----
    clean_query = rewrite_query(query)
    print("✨ Clean Query:", clean_query)
    stable_search(clean_query, num_results)


# ----------------------------
#  TEST
# ----------------------------cd
