import asyncio
import aiohttp
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
import json

# 상태 구조 정의
class State(TypedDict):
    user_input: str
    final_answer: str

# MCP 서버를 SSE로 호출하는 함수
async def sse_invoke(tool: str, params: dict) -> dict:
    url = "[invalid url, do not cite]  # 서버가 다른 포트에서 실행 중이면 URL 조정 필요
    payload = {"tool": tool, "params": params}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            if resp.status != 200:
                return {"error": f"Server returned status {resp.status}"}
            async for line in resp.content:
                if line.startswith(b"data:"):
                    data = line[5:].decode().strip()
                    if data:
                        return json.loads(data)
    return {"error": "No data received"}

# Perplexity에 질문하고 답변을 받는 노드
async def ask_node(state: State) -> dict:
    query = state["user_input"]
    messages = [{"role": "user", "content": query}]
    result = await sse_invoke("perplexity_ask", {"messages": messages})
    if "error" in result:
        return {"final_answer": f"Error: {result['error']}"}
    # 응답 파싱, Perplexity API 응답 형식에 따라 조정
    if "choices" in result and len(result["choices"]) > 0:
        answer = result["choices"][0]["message"]["content"]
    else:
        answer = "No answer received"
    return {"final_answer": answer}

# 상태 그래프 설정
graph = StateGraph(State)
graph.add_node("ask_node", ask_node)
graph.add_edge(START, "ask_node")
graph.add_edge("ask_node", END)
graph = graph.compile()

# 메인 함수, 그래프 실행
async def main():
    user_question = "서울의 내일 날씨는?"  # 예시 질문
    initial_state = {"user_input": user_question}
    result_state = await graph.ainvoke(initial_state)
    print("질문:", user_question)
    print("답변:", result_state.get("final_answer"))

if __name__ == "__main__":
    asyncio.run(main())