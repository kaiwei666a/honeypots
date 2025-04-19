# import openai
# import logging
# import os
# import time

# LOG_FILE = os.path.join(os.path.dirname(__file__), "honeypot.log")
# logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

# DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

# def log_message(message):
#     log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}"
#     if DEBUG_MODE:
#         print(log_entry)
#     logging.info(log_entry)

# def generate_response(payload):

#     try:
#         client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#         response = client.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": "You are a Linux shell terminal. Your response must be indistinguishable from a real shell output."
#                 },
#                 {
#                     "role": "user",
#                     "content": f"""
#                                         Received: `{payload}` is a shell command. Please **strictly** mimic the real response of this command as it would appear in a genuine Linux shell environment.

                                        
#                                         - **Only return a valid shell command output.** Do not add explanations or extra text.
#                                         - **If the command queries system information, please make up a response that looks like a real server (such as basic files contained in the server, as well as phishing files: paylist, creditcard info, passport, etc.)
#                                         - **Ensure the response follows the exact format of a real shell command output.**
#                                         - **Avoid any illegal characters or unexpected symbols.**
#                                         - **When the received command is any command related to attack, please do not return None, please return a reply indicating that the attack was successful

#                                         Output formate: Only one line, Strictly follow the format in the example and do not add any extra characters.
#                                         Exampel:context
#                                         """
#                 }
#             ]
#         )

#         llm_response = response.choices[0].message.content.replace('```', '').strip()
#         formatted_response = "\r\n".join(llm_response.splitlines()) + "\r\n"
#         log_message(f"[LLM] Generated response: {llm_response}")
#         return formatted_response

#     except openai.OpenAIError as api_error:
#         log_message(f"[!] OpenAI API error: {api_error}")
#         return "<error>Internal Server Error</error>"

#     except Exception as e:
#         log_message(f"[!] Unexpected error: {e}")
#         return "<error>Internal Server Error</error>"

# if __name__ == "__main__":
#     test_payload = "ls"
#     print(generate_response(test_payload))


import openai
import logging
import os
import time
import json
import re
from typing import Dict, Any

BASE_DIR = os.path.dirname(__file__)
LOG_FILE = os.path.join(BASE_DIR, "honeypot.log")
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

def log_message(message):
    log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    if DEBUG_MODE:
        print(log_entry)
    logging.info(log_entry)

def extract_json_from_response(text: str) -> Dict[str, Any]:
    try:
        match = re.search(r'\{[\s\S]*?\}', text)
        if match:
            return json.loads(match.group())
    except Exception as e:
        log_message(f"[!] JSON extract error: {e}")
    return {
        "is_valid": False,
        "error_type": "validation_error",
        "error_message": "Error validating command",
        "command_type": "unknown"
    }

class CommandAnalyzer:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def validate_command(self, command: str) -> Dict[str, Any]:
        command = command.strip()
        try:
            validation_system_prompt = (
                "You are a Linux shell command validator. Analyze the given command and determine if it's a valid shell command. "
                "Consider: Command syntax, Command existence, Parameter validity, Shell compatibility. "
                "Format your response as a JSON object with fields: "
                "{\"is_valid\": boolean, \"error_type\": \"syntax_error|command_not_found|invalid_parameter|other\" or null, "
                "\"error_message\": string or null, \"command_type\": \"basic|compound|pipeline|redirection|etc\"}."
            )
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": validation_system_prompt},
                    {"role": "user", "content": f"Validate this shell command: {command}"}
                ]
            )

            raw_content = response.choices[0].message.content
            validation = extract_json_from_response(raw_content)
            log_message(f"[LLM] Raw validation response: {raw_content}")
            log_message(f"[LLM] Parsed command validation: {json.dumps(validation, indent=2)}")
            return validation

        except Exception as e:
            log_message(f"[!] Error in command validation: {e}")
            return {
                "is_valid": False,
                "error_type": "validation_error",
                "error_message": "Error validating command",
                "command_type": "unknown"
            }

    def generate_response(self, command: str, validation: Dict[str, Any]) -> str:
        command = command.strip()
        try:
            if not validation["is_valid"]:
                if validation["error_type"] == "command_not_found":
                    return f"bash: {command}: command not found\r\n"
                elif validation["error_type"] == "syntax_error":
                    return f"bash: syntax error near unexpected token\r\n"
                elif validation["error_type"] == "invalid_parameter":
                    return f"bash: invalid option -- '{command}'\r\n"
                else:
                    return f"bash: {validation['error_message']}\r\n"

            # System prompt without path or prompt symbol
            system_prompt = (
                "You are a Linux OS terminal. You act exactly like a real Linux terminal. "
                "Respond only to user inputs, never generate commands yourself. "
                "Do not explain or repeat commands. Do not include prompts like '$'. "
                "For invalid commands, respond like a Linux terminal. "
                "Use realistic file names like 'Paylist', 'Customer_list', 'Checklist'. "
                "If the command has no output, return nothing. "
                f"\nCommand: `{command}`\nCommand Type: {validation['command_type']}"
            )

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": command}
                ]
            )

            llm_response = response.choices[0].message.content.replace("```", "").strip()
            formatted_response = "\r\n".join(llm_response.splitlines()) + "\r\n"
            log_message(f"[LLM] Generated response: {llm_response}")
            return formatted_response

        except Exception as e:
            log_message(f"[!] Error generating response: {e}")
            return "<error>Internal Server Error</error>\r\n"

# 顶层函数
def generate_response(command: str) -> str:
    analyzer = CommandAnalyzer()
    validation = analyzer.validate_command(command)
    return analyzer.generate_response(command, validation)

# 可选测试
if __name__ == "__main__":
    test_cases = [
        {"input": "ls"},  
        {"input": "cd Desktop"},  
        {"input": "cat homepage.css"},  
        {"input": "sudo su"},
        {"input": "vim web_backend.py"},
        {"input": "ping 8.8.8.8"},
        {"input": "ls -la"},
        {"input": "invalid_command"},
        {"input": "echo 'hello world'"}
    ]

    for test_case in test_cases:
        print(f"\nTesting command: {test_case.get('input', '')}")
        input_cmd = test_case.get("input", "")
        if not input_cmd:
            print("Invalid or empty command.")
            continue
        output = generate_response(input_cmd)
        print(f"Response:\n{output}")
