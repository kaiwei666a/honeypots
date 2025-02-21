import socket
import threading
import time
import logging
from flask import Flask, request
# from urllib.parse import quote as url_quote


# 记录日志文件
LOG_FILE = "activemq_honeypot.log"

# 伪造 Web 控制台（端口 8161）
app = Flask(__name__)

@app.route('/')
def home():
    return "ActiveMQ Web Console (Simulated)", 200

@app.route('/admin')
def admin_panel():
    return "ActiveMQ Admin Panel (Simulated)", 200

# 记录攻击行为
def log_attack(message):
    log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    print(log_entry)
    logging.info(log_entry)

# 伪造 OpenWire 端口（61616），模拟 ActiveMQ RCE 漏洞
def openwire_honeypot():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 61616))
    server.listen(5)
    log_attack("[*] ActiveMQ Honeypot running on port 61616...")

    while True:
        client, addr = server.accept()
        log_attack(f"[*] Connection from {addr[0]}:{addr[1]} on port 61616 (Possible Exploit Attempt)")

        # 读取攻击者的请求数据
        try:
            data = client.recv(4096).decode("utf-8", errors="ignore")
            log_attack(f"[!] Received potential exploit payload: {data}")

            # 伪造漏洞响应，但不执行代码
            if "poc.xml" in data:
                fake_response = b"HTTP/1.1 200 OK\r\nContent-Type: text/xml\r\n\r\n<response>Fake XML Response</response>"
                client.send(fake_response)
                log_attack(f"[!] Sent Fake XML Response to {addr[0]}")

        except Exception as e:
            log_attack(f"[!] Error handling request: {e}")

        finally:
            client.close()

# 运行蜜罐
if __name__ == "__main__":
    # 设置日志
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

    # 启动 OpenWire 监听器（61616端口）线程
    threading.Thread(target=openwire_honeypot, daemon=True).start()

    # 以生产模式运行 Flask，避免 Docker 进程退出
    app.run(host="0.0.0.0", port=8161, debug=False, use_reloader=False)
