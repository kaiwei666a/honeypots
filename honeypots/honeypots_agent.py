import socket
import threading
import time
import logging
import os
import sqlite3
import requests
from llm_response import generate_response
from planning_agent import analyze_logs_and_define_strategy

LOG_FILE = os.path.join(os.path.dirname(__file__), "honeypot.log")
DB_PATH = os.path.join(os.path.dirname(__file__), "honeypot_responses.db")

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def log_attack(message):
    """记录攻击行为"""
    log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    print(log_entry)
    logging.info(log_entry)

def init_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT UNIQUE,
            response TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_to_database(command, response):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT OR IGNORE INTO responses (command, response) VALUES (?, ?)", (command, response))
        conn.commit()
    except Exception as e:
        log_attack(f"[!] Error saving to database: {e}")
    finally:
        conn.close()

def fetch_rag_response(payload):
    """基于 RAG 从数据库或外部数据源检索相关响应，并缓存结果"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT response FROM responses WHERE command = ? LIMIT 1", (payload,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]
    
    # 外部数据
    external_sources = [
        "https://zenodo.org/records/3687527",
        "https://gitlab.ics.muni.cz/muni-kypo-trainings/datasets/commands",
        "https://huggingface.co/datasets/tmskss/linux-man-pages-tldr-summarized"
    ]
    
    for source in external_sources:
        try:
            response = requests.get(source, timeout=5)
            if response.status_code == 200:
                response_text = response.text[:1024]  # 限制返回长度，防止过长数据
                save_to_database(payload, response_text)  # 缓存到本地数据库
                return response_text
        except requests.RequestException as e:
            log_attack(f"[!] Failed to fetch from {source}: {e}")
    

    llm_generated_response = generate_response(payload)
    save_to_database(payload, llm_generated_response) 
    return llm_generated_response

def openwire_honeypot():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 61616))  
    server.listen(5)
    log_attack("[*] ActiveMQ Honeypot running on port 61616...")

    while True:
        try:
            client, addr = server.accept()
            log_attack(f"[*] Connection from {addr[0]}:{addr[1]} (Possible Exploit Attempt)")

            
            data = client.recv(4096).decode("utf-8", errors="ignore")
            log_attack(f"[!] Received potential exploit payload: {data}")

            
            rag_response = fetch_rag_response(data)
            fake_response = f"HTTP/1.1 200 OK\r\nContent-Type: text/xml\r\n\r\n{rag_response}".encode()
            
            client.send(fake_response)
            log_attack(f"[!] Sent RAG-based response to {addr[0]}")

            
            analyze_logs_and_define_strategy()

        except Exception as e:
            log_attack(f"[!] Error handling request: {e}")
        
        finally:
            client.close()

if __name__ == "__main__":
    init_database()
    threading.Thread(target=openwire_honeypot, daemon=True).start()
    while True:
        time.sleep(10)