# import requests
# import openai
# import os
# import json



# # def fetch_data(offset=0, length=100):
# #     """
# #     Retrieve data from the Hugging Face dataset server.
# #     """
# #     url = (
# #         "https://datasets-server.huggingface.co/rows?"
# #         "dataset=tmskss%2Flinux-man-pages-tldr-summarized&"
# #         "config=default&split=train&offset={offset}&length={length}"
# #     ).format(offset=offset, length=length)
    
# #     response = requests.get(url)
# #     if response.ok:
# #         data = response.json()
# #         rows = data.get("rows", [])
# #         print(rows)
# #         return rows
# #     else:
# #         raise Exception("Data request failed with status code: {}".format(response.status_code))
# def fetch_data(offset=0, length=100):
#     url = f"https://datasets-server.huggingface.co/rows?dataset=tmskss%2Flinux-man-pages-tldr-summarized&config=default&split=train&offset={offset}&length={length}"
    
#     response = requests.get(url)
    
#     if response.ok:
#         try:
#             data = response.json()
#             rows = data.get("rows", [])
            
#             if not rows:
#                 print("[!] API 返回了空数据")
#                 return {"error": "No data found", "rows": []}
            

#             print("Fetched Rows:", json.dumps(rows[:5], indent=4, ensure_ascii=False))  
            
#             return {"status": "success", "rows": rows}
        
#         except json.JSONDecodeError as e:
#             print("[!] 解析 JSON 失败:", e)
#             print("[!] API 返回的原始内容:", response.text[:500])  # 只打印前 500 个字符
#             return {"error": "JSON decoding failed", "response": response.text[:500]}
    
#     else:
#         print("[!] 请求失败，状态码:", response.status_code)
#         return {"error": f"Request failed with status {response.status_code}"}


# def generate_filter_prompt(rows, topic="network management"):
#     """
#     Construct a prompt to filter out entries related to the specified topic
#     from the Linux man-pages TLDR data.
#     """
#     prompt = f"Please filter out the commands or instructions related to '{topic}' from the following Linux man-pages TLDR data. Remove duplicates and unrelated content:\n\n"
#     for row in rows:
#         title = row.get('title', '')
#         summary = row.get('summary', '')
#         prompt += f"Title: {title}\nSummary: {summary}\n\n"
#     return prompt

# def call_llm(prompt, model="gpt-4o", max_tokens=500):
#     """
#     Call the LLM with the given prompt and return the generated text.
#     """
#     client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#     response = client.chat.completions.create(

#         model=model,
#         messages=[{"role": "user", "content": prompt}],
#         max_tokens=max_tokens,
#         temperature=0.7
#     )
#     return response.choices[0].message["content"]

# def main():
#     try:
#         rows = fetch_data(offset=0, length=100)
#     except Exception as e:
#         print("Failed to fetch data:", e)
#         return

#     filter_prompt = generate_filter_prompt(rows, topic="network management")
#     print("Filter Prompt:")
#     print(filter_prompt)
    
#     filtered_output = call_llm(filter_prompt)
#     print("Filtered Output:")
#     print(filtered_output)
    
#     gen_prompt = (
#         "Based on the following filtered Linux network management command data, please generate a detailed instruction document. "
#         "Include the purpose of each command, usage scenarios, and examples:\n---\n" + 
#         filtered_output + "\n---\nPlease generate the document."
#     )
#     generated_instructions = call_llm(gen_prompt, max_tokens=800)
#     print("Final Generated Instruction Document:")
#     print(generated_instructions)

# if __name__ == "__main__":
#     main()



import requests
import json

def fetch_data(offset=0, length=100):
    url = f"https://datasets-server.huggingface.co/rows?dataset=tmskss%2Flinux-man-pages-tldr-summarized&config=default&split=train&offset={offset}&length={length}"
    response = requests.get(url)

    if response.ok:
        try:
            data = response.json()
            rows = data.get("rows", [])
            if not rows:
                return {"error": "No data found", "rows": []}
            return {"status": "success", "rows": rows}
        except json.JSONDecodeError as e:
            return {"error": "JSON decoding failed", "response": response.text[:500]}
    else:
        return {"error": f"Request failed with status {response.status_code}"}

def find_command_details(command, total_records=481, batch_size=100): 
    matched_commands = []
    
    for offset in range(0, total_records, batch_size):
        data = fetch_data(offset=offset, length=batch_size)

        if "rows" not in data or not data["rows"]:
            continue  

        for item in data["rows"]:
            row_data = item["row"]
            command_name = row_data.get("Command", "").strip().lower()
            text = row_data.get("Text", "")
            summary = row_data.get("Summary", "")

            if command_name == command.strip().lower():
                matched_commands.append({
                    "command": command_name,
                    "text": text,
                    "summary": summary
                })

    return matched_commands if matched_commands else None





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
#             print(response.text[:500])  # 查看非JSON返回内容
#     else:
#         print(f"Request failed with status {response.status_code}: {response.reason}")
#         print("Response Content (first 500 chars):")
#         print(response.text[:500])

# # 执行测试
# if __name__ == "__main__":
#     fetch_data()

