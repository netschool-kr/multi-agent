import requests
import os

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
headers = {
    "xi-api-key": ELEVENLABS_API_KEY,
}
response = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers)
voices = response.json()
print(voices)
