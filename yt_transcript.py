# yt_transcript.py
from mcp.server.fastmcp import FastMCP
from youtube_transcript_api import YouTubeTranscriptApi
import re

# Create FastMCP server instance (service name: "YouTubeService")
mcp = FastMCP("YouTubeService")

# Define and register the YouTube transcript tool
@mcp.tool()
def get_transcript(video_url: str) -> str:
    """Return the full transcript of the specified YouTube video as a single string."""
    try:
        # Extract the video ID from the URL (supports youtu.be short URLs or v= parameter)
        match = re.search(r"(?:v=|youtu\.be/)([^&/\n?]+)", video_url)
        video_id = match.group(1) if match else video_url  # Assume input is ID if no match
        # Retrieve transcript segments via YouTubeTranscriptApi (preferring Korean, fallback to English)
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
        # Concatenate each segment's 'text' field into a single string
        transcript_text = " ".join(seg['text'] for seg in transcript_list)
        return transcript_text
    except Exception as e:
        return f"(Transcript extraction error: {e})"

if __name__ == "__main__":
    mcp.run(transport="stdio")
