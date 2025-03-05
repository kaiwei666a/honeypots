import openai
import logging
import os
import time

# 设置日志文件（存储在程序目录下）
LOG_FILE = os.path.join(os.path.dirname(__file__), "honeypot.log")

# 配置日志
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")



def log_message(message):
    """记录日志"""
    log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    print(log_entry)
    logging.info(log_entry)

def generate_response(payload):
    """使用 LLM 生成动态响应"""
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an ActiveMQ server. Please respond to user requests in technical terms."},
                {"role": "user", "content": f"recive: {payload}，response is waht？"}
            ]
        )
        # ✅ 改为使用属性访问，而不是字典下标访问
        llm_response = response.choices[0].message.content
        log_message(f"[LLM] Generated response: {llm_response}")
        return llm_response
    except Exception as e:
        log_message(f"[!] LLM generate error: {e}")
        return "<error>Internal Server Error</error>"

if __name__ == "__main__":
    test_payload = "test payload"
    print(generate_response(test_payload))
