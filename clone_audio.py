import requests
import json
import os

api_key = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJiZWxsb3JjaGlkIiwiVXNlck5hbWUiOiJiZWxsb3JjaGlkIiwiQWNjb3VudCI6IiIsIlN1YmplY3RJRCI6IjE5MzQ4NjQ0NDUxNjM0NDI5NzAiLCJQaG9uZSI6IjE3NjgyMzE4NDczIiwiR3JvdXBJRCI6IjE5MzQ4NjQ0NDUxNTUwNTQzNjIiLCJQYWdlTmFtZSI6IiIsIk1haWwiOiIiLCJDcmVhdGVUaW1lIjoiMjAyNS0wNi0yNiAxNjowMTo0MyIsIlRva2VuVHlwZSI6MSwiaXNzIjoibWluaW1heCJ9.N__rzJWQ8qhHOLU3elUggJ8ZY8qqcaFIiPNDDf7upEvAEVxeQYbXilb-PqU9Eap4MlU-k7IyYIuviT0VC5j3aaLqTmWX5V6OKEmrRF0WeEt9LjZqpB_rglfVzy5SYKj5-lS4Z8DK6Exix8zB4wUXslp_bgLfaqULRWksWv-CbQsHanwLaMS7fFhY0rAn2l-KonyHsNQcuDFMsGMCs5e4TG3g7A4EZNfvSsiw7Mwq5ek-DGAzOBMbW8jE49Y73SYKeB4JNEn9WYUmTtuN2vfdQPw1RPBI4O3-Snf4vWGzOVATx1rNA-tHxfiHe6cV31UI50NKHFW7S11EdNqXGnQEig"
url = "https://api.minimaxi.com/v1/voice_clone"

clone_payload = {
    "file_id": 331195287064988,
    "voice_id": "wq_20251106",
    "model": "speech-2.6-hd"
}
clone_headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.post(url, headers=clone_headers, json=clone_payload)
response.raise_for_status()
print(response.text)