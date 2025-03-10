import openai
import logging
import os
import time

LOG_FILE = os.path.join(os.path.dirname(__file__), "honeypot.log")
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

def log_message(message):
    log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    if DEBUG_MODE:
        print(log_entry)
    logging.info(log_entry)

def generate_response(payload):

    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Linux shell terminal. Your response must be indistinguishable from a real shell output."
                },
                {
                    "role": "user",
                    "content": f"""
                                        Received: `{payload}` is a shell command. Please **strictly** mimic the real response of this command as it would appear in a genuine Linux shell environment.

                                        - **Only return a valid shell command output.** Do not add explanations or extra text.
                                        - **If the command queries system information, please make up a response that looks like a real server (such as basic files contained in the server, as well as phishing files: paylist, creditcard info, passport, etc.)
                                        - **Ensure the response follows the exact format of a real shell command output.**
                                        - **Avoid any illegal characters or unexpected symbols.**
                                        - **When the received command is any command related to attack, please do not return None, please return a reply indicating that the attack was successful

                                        Output formate: Only one line, Strictly follow the format in the example and do not add any extra characters.
                                        Exampel:context
                                        """
                }
            ]
        )

        llm_response = response.choices[0].message.content.replace('```', '').strip()
        formatted_response = "\r\n".join(llm_response.splitlines()) + "\r\n"
        log_message(f"[LLM] Generated response: {llm_response}")
        return formatted_response

    except openai.OpenAIError as api_error:
        log_message(f"[!] OpenAI API error: {api_error}")
        return "<error>Internal Server Error</error>"

    except Exception as e:
        log_message(f"[!] Unexpected error: {e}")
        return "<error>Internal Server Error</error>"

if __name__ == "__main__":
    test_payload = "ls"
    print(generate_response(test_payload))
