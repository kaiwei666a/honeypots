import requests
import json

url = "https://datasets-server.huggingface.co/rows?dataset=tmskss%2Flinux-man-pages-tldr-summarized&config=default&split=train&offset=0&length=100"

response = requests.get(url)

if response.ok:
    try:
        data = response.json()
        rows = data.get("rows", [])
        print(f"Rows retrieved: {len(rows)}")
        for row in rows:
            print(json.dumps(row, indent=2))
    except json.JSONDecodeError as e:
        print(f"JSON decoding failed: {e}")
else:
    print(f"Request failed with status code {response.status_code}: {response.reason}")