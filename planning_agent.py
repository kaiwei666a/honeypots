import openai
import os
import logging
import time
from pathlib import Path
from googlesearch import search  

BASE_DIR = Path(__file__).parent.resolve()
LOG_FILE = BASE_DIR / "honeypot.log"
DEFENSE_FILE = BASE_DIR / "define_log.txt"

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def log_message(message):
    log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    print(log_entry)
    logging.info(log_entry)

def read_logs():
    try:
        if LOG_FILE.exists():
            with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
                logs = f.readlines()[-10:]  
            return "\n".join(logs)
        else:
            log_message("[!] didnt find logs")
            return "no logs"
    except Exception as e:
        log_message(f"[!] read logs error: {e}")
        return ""

def search_defense_strategies(attacker_input):
    try:
        query = f"how to protect against {attacker_input} attack"
        results = list(search(query, num_results=3))  
        return results
    except Exception as e:
        log_message(f"[!] search error: {e}")
        return []

def define_defense_strategy(logs, search_results, attacker_input):
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert responsible for designing a defense strategy against detected attacks."},
                {"role": "user", "content": f"""
                Detected attacker activity: `{attacker_input}`

                ### Recent Attack Logs:
                {logs}

                ### Relevant Cybersecurity Insights:
                {search_results}

                ### Task:
                - Analyze the attack pattern and identify potential vulnerabilities.
                - Generate **specific, actionable defense strategies** to mitigate the attack.
                - Provide security measures that can be **immediately implemented** to strengthen the honeypot.
                - Ensure the response follows industry best practices and does not include generic or vague recommendations.
                - Format the response in a structured manner (e.g., step-by-step instructions, firewall rules, intrusion detection rules, system hardening tips).

                Return a **detailed and executable security plan** that effectively counters the detected threat.
                 
                 """}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        log_message(f"[!] LLM error in defining strategy: {e}")
        return "No effective defense strategy generated."

def analyze_logs_and_define_strategy(attacker_input):
    logs = read_logs()
    search_results = search_defense_strategies(attacker_input)
    defense_strategy = define_defense_strategy(logs, search_results, attacker_input)
    
    with open(DEFENSE_FILE, "w", encoding="utf-8") as f:
        f.write(defense_strategy)
    
    log_message(f"[!] Updated defense strategy: {defense_strategy}")

if __name__ == "__main__":
    attacker_input = input("Enter the attack command or pattern detected: ")
    analyze_logs_and_define_strategy(attacker_input)
