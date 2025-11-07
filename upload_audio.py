import requests
import os

api_key = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJiZWxsb3JjaGlkIiwiVXNlck5hbWUiOiJiZWxsb3JjaGlkIiwiQWNjb3VudCI6IiIsIlN1YmplY3RJRCI6IjE5MzQ4NjQ0NDUxNjM0NDI5NzAiLCJQaG9uZSI6IjE3NjgyMzE4NDczIiwiR3JvdXBJRCI6IjE5MzQ4NjQ0NDUxNTUwNTQzNjIiLCJQYWdlTmFtZSI6IiIsIk1haWwiOiIiLCJDcmVhdGVUaW1lIjoiMjAyNS0wNi0yNiAxNjowMTo0MyIsIlRva2VuVHlwZSI6MSwiaXNzIjoibWluaW1heCJ9.N__rzJWQ8qhHOLU3elUggJ8ZY8qqcaFIiPNDDf7upEvAEVxeQYbXilb-PqU9Eap4MlU-k7IyYIuviT0VC5j3aaLqTmWX5V6OKEmrRF0WeEt9LjZqpB_rglfVzy5SYKj5-lS4Z8DK6Exix8zB4wUXslp_bgLfaqULRWksWv-CbQsHanwLaMS7fFhY0rAn2l-KonyHsNQcuDFMsGMCs5e4TG3g7A4EZNfvSsiw7Mwq5ek-DGAzOBMbW8jE49Y73SYKeB4JNEn9WYUmTtuN2vfdQPw1RPBI4O3-Snf4vWGzOVATx1rNA-tHxfiHe6cV31UI50NKHFW7S11EdNqXGnQEig"
url = "https://api.minimaxi.com/v1/files/upload"

payload = {"purpose": "voice_clone"}
files = [
  ("file", ("clone_input.mp3", open("/Volumes/工作文档/长根堂按日期文件夹/2025-11-06-王董声音克隆/WQ-ORI.MP3", "rb")))
]
headers = {
  "Authorization": f"Bearer {api_key}"
}

response = requests.post(url, headers=headers, data=payload, files=files)
response.raise_for_status()
file_id = response.json().get("file", {}).get("file_id")
print(file_id)