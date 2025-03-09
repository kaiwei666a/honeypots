import openai
import os
import logging
import time
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
DEFENSE_FILE = BASE_DIR / "define_log.txt"
PROTECTION_SCRIPT = BASE_DIR / "honeypot_protection.sh"

logging.basicConfig(filename=BASE_DIR / "honeypot.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_message(message):
    log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    print(log_entry)
    logging.info(log_entry)

def read_defense_log():
    try:
        if DEFENSE_FILE.exists():
            with open(DEFENSE_FILE, "r", encoding="utf-8", errors="ignore") as f:
                return f.read().strip()
        else:
            log_message("[!] Defense log not found.")
            return ""
    except Exception as e:
        log_message(f"[!] Error reading defense log: {e}")
        return ""

def generate_protection_script(defense_log):

    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a cybersecurity automation system. Based on the provided defense strategies, generate a Bash script to implement the protections."},
                {"role": "user", "content": f"Defense Strategy:\n{defense_log}\n\nGenerate a secure and effective Linux shell script to apply these protections."}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        log_message(f"[!] Error generating protection script: {e}")
        return ""

def save_protection_script(script_content):
    try:
        with open(PROTECTION_SCRIPT, "w", encoding="utf-8") as f:
            f.write(script_content)
        log_message(f"[+] Protection script saved: {PROTECTION_SCRIPT}")
    except Exception as e:
        log_message(f"[!] Error saving protection script: {e}")

def apply_protection():
    defense_log = read_defense_log()
    if not defense_log:
        log_message("[!] No valid defense strategy found.")
        return
    
    protection_script = generate_protection_script(defense_log)
    if protection_script:
        save_protection_script(protection_script)
        os.chmod(PROTECTION_SCRIPT, 0o755)
        log_message("[+] Applying protection script...")
        os.system(f"bash {PROTECTION_SCRIPT}")
    else:
        log_message("[!] Protection script generation failed.")

if __name__ == "__main__":
    apply_protection()
