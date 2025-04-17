# elevenlabs_mcp_server.py
from mcp.server.fastmcp import FastMCP
import os, requests
from dotenv import load_dotenv, find_dotenv

# .env 파일에서 TAVILY_API_KEY, SERPAPI_API_KEY 등을 로드
load_dotenv(find_dotenv())
mcp = FastMCP("ElevenLabsAPI")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
DEFAULT_VOICE_ID = os.getenv("ELEVENLABS_DEFAULT_VOICE_ID")

@mcp.tool()
def synthesize_speech(text: str, voice_id: str = None) -> dict:
    """
    주어진 텍스트를 ElevenLabs API를 통해 음성으로 변환합니다.
    
    파라미터:
    - text: 음성으로 변환할 텍스트
    - voice_id: 사용할 목소리 ID (입력하지 않으면 기본값 사용)
    
    반환:
    - API 응답 JSON (예: 오디오 파일 URL 등)
    """
    if voice_id is None:
        voice_id = DEFAULT_VOICE_ID
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_settings": {  # 예시 파라미터: 안정성 및 유사도 boost 값 등
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        # 서버에 오디오 파일 저장
        output_file = f"output_{voice_id}_{hash(text) % 10000}.mp3"  # 고유 파일명 생성
        try:
            with open(output_file, "wb") as f:
                f.write(response.content)
            return {
                "status": "success",
                "content_type": response.headers.get("Content-Type"),
                "file_path": output_file,
                "message": f"Audio saved on server as {output_file}"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Failed to save audio file: {str(e)}"
            }
    else:
        # 오류 시 JSON 파싱 시도
        try:
            data = response.json()
        except Exception as e:
            data = {"error": str(e), "response_text": response.text}
        return {"status": "error", "data": data}
    
if __name__ == "__main__":
    mcp.run(transport="stdio")
