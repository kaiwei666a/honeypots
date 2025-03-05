import openai
import os
import logging
import time
from pathlib import Path
from googlesearch import search  # 可替换成其他搜索 API

# 定义日志和防御策略文件路径
BASE_DIR = Path(__file__).parent.resolve()
LOG_FILE = BASE_DIR / "honeypot.log"
DEFENSE_FILE = BASE_DIR / "define_log.txt"

# 设置日志记录
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")


def log_message(message):
    """记录日志"""
    log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    print(log_entry)
    logging.info(log_entry)


def read_logs():
    """读取蜜罐日志并提取最近的攻击记录"""
    try:
        if LOG_FILE.exists():
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = f.readlines()[-10:]  # 只读取最近 10 条日志
            return "\n".join(logs)
        else:
            log_message("[!] 没有找到日志文件")
            return "没有日志记录。"
    except Exception as e:
        log_message(f"[!] 读取日志失败: {e}")
        return ""


def search_defense_strategies():
    """从网上搜索蜜罐防御策略"""
    try:
        query = "如何防御 ActiveMQ 蜜罐攻击"
        results = list(search(query, num_results=3))  # 限制搜索结果为 3 个
        return results
    except Exception as e:
        log_message(f"[!] 搜索防御策略失败: {e}")
        return []


def define_defense_strategy(logs, search_results):
    """使用 OpenAI 生成防御策略"""
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # 发送请求到 GPT-4o 生成防御策略
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a security expert responsible for developing a defense strategy for the ActiveMQ honeypot."},
                {"role": "user", "content": f"attack logs:\n{logs}\n\nfrom network result:\n{search_results}\n\nanalyze and generate defense method."}
            ]
        )

        return response.choices[0].message.content
    except Exception as e:
        log_message(f"[!] LLM 生成防御策略失败: {e}")
        return "未能生成防御策略。"


def analyze_logs_and_define_strategy():
    """读取日志，搜索防御策略，并生成最终防御措施"""
    logs = read_logs()
    search_results = search_defense_strategies()
    defense_strategy = define_defense_strategy(logs, search_results)

    # 保存防御策略
    with open(DEFENSE_FILE, "w", encoding="utf-8") as f:
        f.write(defense_strategy)

    log_message(f"[!] renew defense: {defense_strategy}")


# 主函数调用
if __name__ == "__main__":
    analyze_logs_and_define_strategy()