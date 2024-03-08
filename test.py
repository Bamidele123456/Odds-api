import requests


API_URL = "https://hh0pa0lb9sed7tc5.us-east-1.aws.endpoints.huggingface.cloud"
headers = {"Accept": "application/json", "Content-Type": "application/json"}
payload = {
    "inputs": "who would win this match today Everton vs Crystal Palace","parameters": {"temperature": 0.1}}
response = requests.post(API_URL, headers=headers, json=payload)
print(response.json())