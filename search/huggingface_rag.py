
# import requests
# import json

# def fetch_data(offset=0, length=100):
#     url = f"https://datasets-server.huggingface.co/rows?dataset=tmskss%2Flinux-man-pages-tldr-summarized&config=default&split=train&offset={offset}&length={length}"
#     response = requests.get(url)

#     if response.ok:
#         try:
#             data = response.json()
#             rows = data.get("rows", [])
#             if not rows:
#                 return {"error": "No data found", "rows": []}
#             return {"status": "success", "rows": rows}
#         except json.JSONDecodeError as e:
#             return {"error": "JSON decoding failed", "response": response.text[:500]}
#     else:
#         return {"error": f"Request failed with status {response.status_code}"}

# def find_command_details(command, total_records=481, batch_size=100): 
#     matched_commands = []
    
#     for offset in range(0, total_records, batch_size):
#         data = fetch_data(offset=offset, length=batch_size)

#         if "rows" not in data or not data["rows"]:
#             continue  

#         for item in data["rows"]:
#             row_data = item["row"]
#             command_name = row_data.get("Command", "").strip().lower()
#             text = row_data.get("Text", "")
#             summary = row_data.get("Summary", "")

#             if command_name == command.strip().lower():
#                 matched_commands.append({
#                     "command": command_name,
#                     "text": text,
#                     "summary": summary
#                 })

#     return matched_commands if matched_commands else None





# import requests

# def fetch_data(offset=0, length=100):
#     url = f"https://datasets-server.huggingface.co/rows?dataset=tmskss%2Flinux-man-pages-tldr-summarized&config=default&split=train&offset={offset}&length={length}"
#     print(f"Requesting URL: {url}")

#     response = requests.get(url, timeout=10)

#     if response.ok:
#         try:
#             data = response.json()
#             print("JSON data received successfully.")
#             print(data)
#             return data
#         except ValueError:
#             print("Response is not JSON format!")
#             print("Response Content (first 500 chars):")
#             print(response.text[:500]) 
#     else:
#         print(f"Request failed with status {response.status_code}: {response.reason}")
#         print("Response Content (first 500 chars):")
#         print(response.text[:500])

# if __name__ == "__main__":
#     fetch_data()


import openai
import requests
import json
import os

def extract_command_from_text(text):

    prompt = (
        "Extract the main command from the following command line input (executable file, "
        "which can be executed in the Linux shell, and the rest can be ignored) "
        "and output only the command:\n\n"
        f"{text}\n\nCommand:"
    )
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert assistant specialized in extracting commands from command line inputs."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
    )
    main_command = response.choices[0].message.content.strip()
    return main_command

def fetch_data(offset=0, length=100):
    url = (
        f"https://datasets-server.huggingface.co/rows?"
        f"dataset=tmskss%2Flinux-man-pages-tldr-summarized&config=default&split=train"
        f"&offset={offset}&length={length}"
    )
    response = requests.get(url)
    if response.ok:
        try:
            data = response.json()
            rows = data.get("rows", [])
            if not rows:
                return None
            return rows
        except json.JSONDecodeError:
            return None
    return None

def find_command_details(user_input, total_records=481, batch_size=100):

    main_command = extract_command_from_text(user_input)
    if not main_command:
        return {"input": user_input, "error":"can not extrace"}

    matched_commands = []
    for offset in range(0, total_records, batch_size):
        data = fetch_data(offset=offset, length=batch_size)
        if not data:
            continue

        for item in data:
            row_data = item["row"]
            command_name = row_data.get("Command", "").strip().lower()
            text = row_data.get("Text", "")
            summary = row_data.get("Summary", "")
            if command_name == main_command.lower():
                matched_commands.append({
                    "command": command_name,
                    "text": text,
                    "summary": summary
                })
    return {"input": user_input, "matches": matched_commands if matched_commands else None}
