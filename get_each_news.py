import os
import json
import openai
import schedule
import time
from newsapi import NewsApiClient
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List  
from dotenv import load_dotenv  
load_dotenv() 

# ✅ 1. 공유 정보 (State) 정의
class NewsState(TypedDict):  
    user_input: str  
    topic: str  
    model: str  
    max_articles: int  
    articles: List[dict]  
    news: List[dict]  
    save_path: str  

def create_initial_state(user_input: str) -> NewsState:  
    return {  
        "user_input": user_input,  
        "topic": "AI Agent",  
        "model": "gpt-3.5-turbo",  
        "max_articles": 5,  
        "articles": [],  
        "news": [],  
        "save_path": "news_.json"  
    }  
    
# ✅ 2. OpenAI API 설정
openai.api_key = os.environ.get("OPENAI_API_KEY")
MODEL_NAME="gpt-4"#"gpt-3.5-turbo"  
client = openai.Client(api_key=openai.api_key)

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

# ✅ 3. 뉴스 검색 (Fetch News)
import os
import requests
import re

def clean_topic(topic):
    return re.sub('[^a-zA-Z0-9 ]', '', topic).strip()

def fetch_news(state):
    cleaned_topic = clean_topic(state['topic'])
    print(f"📡 '{cleaned_topic}' 관련 최신 뉴스 검색 중...")
    try:
        url = "https://gnews.io/api/v4/search"
        params = {
            "q": cleaned_topic,
            "lang": "en",
            "sortby": "publishedAt",
            "max": state['max_articles'],
            "token": os.environ.get("GNEWS_API_KEY")
        }
        response = requests.get(url, params=params)
        data = response.json()
        state["articles"] = data.get("articles", [])
    except Exception as e:
        print(f"❌ 뉴스 검색 실패: {e}")
        state["articles"] = []
    return state

# newsapi = NewsApiClient(api_key=os.environ.get("NEWSAPI_KEY"))
# import re  
# def clean_topic(topic):  
#     return re.sub('[^a-zA-Z0-9 ]', '', topic).strip()  

# def fetch_news(state: NewsState) -> NewsState:  
#     cleaned_topic = clean_topic(state['topic'])  
#     print(f"📡 '{cleaned_topic}' 관련 최신 뉴스 검색 중...")  
#     try:  
#         response = newsapi.get_everything(q=cleaned_topic, language="en", sort_by="publishedAt", page_size=state['max_articles'])  
#         state["articles"] = response.get('articles', [])  
#     except Exception as e:  
#         print(f"❌ 뉴스 검색 실패: {e}")  
#         state["articles"] = []  
#     return state  


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
                max_tokens=150,  
                temperature=0.5  
            )  
            translation = completion.choices[0].message.content.strip()  
        except Exception as e:  
            print(f"❌ Translation failed: {e}")  
            news = "translation failed"  
        
        translations.append({"title": title, "url": article.get('url'), "content": translation})

    state['news'] = translations
    return state

# ✅ 5. HITL을 활용한 파일명 입력
def get_save_filename(state: NewsState):
    topic_filename = state['topic'].replace(' ', '_')
    state['save_path'] = topic_filename + ".json"
    return state
    # """사용자로부터 저장할 파일명을 입력받음"""
    # print("\n💾 저장할 파일 이름을 입력하세요 (기본값: 'news_summary.json'):")
    # filename = input("👉 ")
    # state['save_path'] = filename.strip() if filename.strip() else "news_summary.json"
    # return state

# ✅ 6. 뉴스 요약 결과 저장
def json_to_markdown(topic, json_file):
    # JSON 파일 읽기 (UTF-8 인코딩)
    with open(json_file, 'r', encoding='utf-8') as file:
        news_list = json.load(file)
    
    # Markdown 형식의 게시글 생성
    markdown_output = f"# 오늘의 {topic} 주요 뉴스\n\n"
    for idx, article in enumerate(news_list, start=1):
        markdown_output += f"### {idx}. {article['title']}\n"
        markdown_output += f"URL: {article['url']}\n"
        markdown_output += f"내용: {article['content']}\n\n"
    
    # 입력 JSON 파일명에서 확장자를 제거하고 .md 확장자로 변경
    base_name = os.path.splitext(json_file)[0]
    md_file = f"{base_name}.md"
    
    # Markdown 파일로 저장
    with open(md_file, 'w', encoding='utf-8') as file:
        file.write(markdown_output)
    
    print(f"Markdown 파일 '{md_file}' 저장 완료!")

def save_news(state: NewsState):
    """요약된 기사들을 JSON 파일로 저장"""
    print(f"📁 '{state['save_path']}' 파일로 저장 중...")
    with open(state['save_path'], "w", encoding="utf-8") as f:
        json.dump(state['news'], f, ensure_ascii=False, indent=2)

    json_to_markdown(state['topic'], state['save_path'])
    print(f"✅ {len(state['news'])}개의 뉴스가 저장되었습니다.")
    return state

# ✅ 7. Edge 연결 및 LangGraph Workflow 구성
workflow = StateGraph(NewsState)

workflow.add_node("parse_user_input", parse_user_input)
workflow.add_node("fetch_news", fetch_news)
workflow.add_node("translate_news", translate_news)
workflow.add_node("get_save_filename", get_save_filename)
workflow.add_node("save_news", save_news)

workflow.add_edge(START, "parse_user_input")
workflow.add_edge("parse_user_input", "fetch_news")
workflow.add_edge("fetch_news", "translate_news")
workflow.add_edge("translate_news", "get_save_filename")
workflow.add_edge("get_save_filename", "save_news")
workflow.add_edge("save_news", END)

graph = workflow.compile()

# ✅ 8. 실행 함수
def run_news_job():
    topics = ["AI Agent", "humanoid", "autonomous driving"]
    for topic in topics:
        initial_state = create_initial_state(topic)
        final_state = graph.invoke(initial_state)

# def run_news_job():
#     """LangGraph 기반 뉴스 요약 워크플로우 실행"""
#     option = input("\n💬 뉴스 검색 요청을 입력하세요 (1: AI Agent, 2: Robot, 3: 자율주행):\n👉 ")
    
#     # 입력값이 1, 2, 3 중 하나면 해당 문자열로 변환, 그렇지 않으면 default로 "AI Agent" 사용
#     mapping = {"1": "AI Agent", "2": "Robot", "3": "자율주행"}
#     user_input = mapping.get(option, "AI Agent")
    
#     initial_state = create_initial_state(user_input)  
#     final_state = graph.invoke(initial_state)
    

run_news_job()

#  ✅ 9. 자동 실행 스케줄링
# schedule.every().day.at("09:00").do(run_news_summary_job)
# print("\n⏳ 뉴스 요약 에이전트 실행 준비 완료! 매일 09:00에 실행됩니다.")

# # ✅ 10. 무한 루프 실행 (스케줄 유지)
# while True:
#     schedule.run_pending()
#     time.sleep(60)
