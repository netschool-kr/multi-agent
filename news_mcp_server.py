# news_mcp_server.py - 뉴스 API MCP 서버 예시
from mcp.server.fastmcp import FastMCP
import os, requests

mcp = FastMCP("NewsAPI")  # MCP 서버 이름 정의

NEWS_API_KEY = os.getenv("NEWS_API_KEY")  # NewsAPI 키 (환경변수에서 읽기)

@mcp.tool()
def get_top_headlines(country: str = "us", category: str = None, q: str = None) -> dict:
    """뉴스 API로 최신 헤드라인 기사 목록을 가져옵니다."""
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {"apiKey": NEWS_API_KEY, "country": country}
    if category:
        params["category"] = category
    if q:
        params["q"] = q  # 키워드 검색어
    res = requests.get(base_url, params=params)
    data = res.json()
    return data  # JSON 그대로 반환 (status, articles 등 포함)

if __name__ == "__main__":
    mcp.run(transport="stdio")  # 표준 입출력을 통해 MCP 서버 실행
