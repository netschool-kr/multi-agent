import os
import json
import openai
import schedule
import time
from newsapi import NewsApiClient
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List  
from dotenv import load_dotenv  
import requests
import re

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")
MODEL_NAME="gpt-4"#"gpt-3.5-turbo"  
client = openai.Client(api_key=openai.api_key)

class NewsState(TypedDict):
    user_input: str
    topic: str
    topics: List[str]
    model: str
    max_articles: int
    articles: List[dict]
    news: List[dict]
    save_path: str

def create_initial_state(input_data) -> NewsState:
    if isinstance(input_data, str):
        initial_state= {
            "user_input": input_data,
            "topic": input_data,
            "topics": [],
            "model": MODEL_NAME,
            "max_articles": 20,
            "articles": [],
            "news": [],
            "save_path": "news_.json"
        }
    elif isinstance(input_data, list):
        initial_state = {
            "user_input": "",
            "topic": "",
            "topics": input_data,
            "model": MODEL_NAME,
            "max_articles": 10,
            "articles": [],
            "news": [],
            "save_path": "news_.json"
        }
    else:
        raise ValueError("Input must be a string or a list of strings")
    
    print("initial_state=", initial_state)
    return initial_state

def clean_topic(topic):
    return re.sub(r'[^\w\s-]', '', topic).strip()

def fetch_news(state):
    if 'topics' in state and state['topics']:
        topics = state['topics']
    else:
        topics = [state['topic']] if state['topic'] else []
    
    cleaned_topics = [clean_topic(topic) for topic in topics]
    cleaned_topics = [topic for topic in cleaned_topics if topic.strip()]
    cleaned_topics = list(set(cleaned_topics))
    
    if not cleaned_topics:
        print("No valid topics provided.")
        state["articles"] = []
        return state
    
    quoted_topics = ['"' + topic + '"' for topic in cleaned_topics]
    query = ' OR '.join(quoted_topics)
    
    print(f"📡 '{', '.join(cleaned_topics)}' related news search in progress...")
    
    try:
        url = "https://gnews.io/api/v4/search"
        params = {
            "q": query,
            "lang": "en",
            "sortby": "publishedAt",
            "max": state['max_articles'],
            "token": os.environ.get("GNEWS_API_KEY")
        }
        response = requests.get(url, params=params)
        data = response.json()
        state["articles"] = data.get("articles",[])
    except Exception as e:
        print(f"❌ News search failed: {e}")
        state["articles"] = []
    return state

def get_save_filename(state: NewsState):
    if 'topics' in state and state['topics']:
        topics_str = '_'.join([topic.replace(' ', '_') for topic in state['topics']])
        state['save_path'] = topics_str + ".json"
    else:
        topic_filename = state['topic'].replace(' ', '_')
        state['save_path'] = topic_filename + ".json"
    return state

def save_news(state: NewsState):
    print(f"Saving to '{state['save_path']}'...")
    with open(state['save_path'], "w", encoding="utf-8") as f:
        json.dump(state['news'], f, ensure_ascii=False, indent=2)
    
    topic_str = ', '.join(state['topics']) if state['topics'] else state['topic']
    json_to_markdown(topic_str, state['save_path'])
    
    print(f"Saved {len(state['news'])} news articles.")
    return state
def extract_cleaned_sentence(text):
    colon_pos = text.find(':')
    if colon_pos == -1:
        return text
    after_colon = text[colon_pos + 1:].strip()  # 콜론 이후의 텍스트를 추출하고 앞뒤 공백 제거
    last_open_bracket = after_colon.rfind('[')  
    if last_open_bracket != -1:  
        cleaned_text = after_colon[:last_open_bracket].rstrip()  
    else:  
        cleaned_text = after_colon
    return cleaned_text  # 마침표가 없을 경우 전체 텍스트 반환
    
def json_to_markdown(topic, json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        news_list = json.load(file)
    5
    markdown_output = ""
    for idx, article in enumerate(news_list, start=1):
        markdown_output += f"{idx}. {article['title']}\n"
        markdown_output += f"{article['url']}\n"
        markdown_output += extract_cleaned_sentence(f"{article['content']}")+"\n\n"
    
    base_name = os.path.splitext(json_file)[0]
    md_file = f"{base_name}.md"
    
    with open(md_file, 'w', encoding='utf-8') as file:
        file.write(markdown_output)
    
    print(f"Markdown file '{md_file}' saved!")


def parse_user_input(state: NewsState) -> NewsState:  
    # print(f"🧠 사용자의 요청을 분석 중: '{state['user_input']}'")  
    # prompt = f"""  
    # 사용자가 다음과 같이 요청했어: "{state['user_input']}"  
    # 1. 이 문장에서 사용자가 검색하려고 하는는 핵심 키워드를 추출해줘.  
    # 2. 예를 들어 "AI Agent, robot, 자율주행에 대한 최신 뉴스 검색해서 파일로 저장해줘"라고 하면 "AI Agent, robot, 자율주행"를 추출해야 해.  
    # 3. 키워드만 한 단어 또는 간결한 문장으로 출력해줘.  
    # """  
    # completion = client.chat.completions.create(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])  
    # if completion.choices and completion.choices[0].message and completion.choices[0].message.content:  
    #     response = completion.choices[0].message.content  
    #     extracted_topic = response.strip()  
    #     if extracted_topic:  
    #         state["topic"] = extracted_topic  
    #     else:  
    #         state["topic"] = "AI Agent"  # 기본값 설정  
    # else:  
    #     state["topic"] = "AI Agent"  # 기본값 설정  
    # print(f"🔍 추출된 뉴스 검색 주제: {state['topic']}")  

    state["topic"] = state['user_input']  

    return state  


# ✅ 4. 뉴스 요약 (Summarize News)
def translate_news(state: NewsState):
    """OpenAI LLM을 사용하여 뉴스 요약"""
    print("📝 뉴스 번역 진행 중...")
    translations = []
    
    for article in state['articles']:
        title = article.get('title', '제목 없음')
        description = article.get('description', '')
        content = article.get('content', '')
        text_to_translate = content if content else (description if description else title)
        
        try:  
            completion = client.chat.completions.create(  
                model=state['model'],  
                messages=[  
                    {"role": "system", "content": "You are a Korean translation assistant. Please Translate the news article to Korean ."},  
                    {"role": "user", "content": f"News article to translate: {text_to_translate}"}  
                    # {"role": "system", "content": "You are a news summary assistant. Please summarize the news article."},  
                    # {"role": "user", "content": f"News article to summarize: {text_to_summarize}"}  
                ],  
                max_tokens=500,  
                temperature=0.5  
            )  
            translation = completion.choices[0].message.content.strip()  
        except Exception as e:  
            print(f"❌ Translation failed: {e}")  
            news = "translation failed"  
        
        translations.append({"title": title, "url": article.get('url'), "content": translation})

    state['news'] = translations
    return state
    
    
# ✅ 7. Edge 연결 및 LangGraph Workflow 구성
workflow = StateGraph(NewsState)

workflow.add_node("fetch_news", fetch_news)
workflow.add_node("translate_news", translate_news)
workflow.add_node("get_save_filename", get_save_filename)
workflow.add_node("save_news", save_news)

workflow.add_edge(START, "fetch_news")
workflow.add_edge("fetch_news", "translate_news")
workflow.add_edge("translate_news", "get_save_filename")
workflow.add_edge("get_save_filename", "save_news")
workflow.add_edge("save_news", END)

graph = workflow.compile()

# ✅ 8. 실행 함수
def run_news_job():
    topics = ["physical ai", "humanoid","AI Agent","tesla", "nvidia",   "fsd", "autonomous driving"]
    initial_state = create_initial_state(topics)
    final_state = graph.invoke(initial_state)
    
run_news_job()