

# test http

# import os
# import time
# import logging
# import threading
# import sqlite3
# from flask import Flask, request, Response
# from llm_response import generate_response
# from planning_agent import analyze_logs_and_define_strategy
# from search.huggingface_rag import fetch_data, find_command_details


# BASE_DIR = os.path.dirname(__file__)
# LOG_FILE = os.path.join(BASE_DIR, "honeypot.log")
# DB_PATH = os.path.join(BASE_DIR, "honeypot_responses.db")


# logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")


# STATIC_RESPONSES = {
#     "get /": "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nRequest successful.",
#     "get /index.html": "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>Index Page</h1></body></html>",
#     "get /about": "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nThis is the about page.",
#     "post /login": "HTTP/1.1 403 Forbidden\r\nContent-Type: text/html\r\n\r\nAccess denied.",
#     "post /submit": "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nSubmission received.",
#     "ssh-2.0-openssh_8.2": "Permission denied.",
#     "ftp login": "530 Login incorrect.",
#     "ping": "PONG",
#     "quit": "Goodbye!",
# }


# def log_attack(message):
#     try:
#         safe_message = message.encode("utf-8", errors="replace").decode("utf-8")
#     except Exception:
#         safe_message = "[ERROR: log encoding failed]"
#     log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {safe_message}"
#     print(log_entry)
#     logging.info(log_entry)


# def init_database():
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS responses (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             command TEXT UNIQUE,
#             response TEXT
#         )
#     """)
#     conn.commit()
#     conn.close()


# def save_to_database(command, response):
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     try:
#         cursor.execute("INSERT OR IGNORE INTO responses (command, response) VALUES (?, ?)", (command, response))
#         conn.commit()
#     except Exception as e:
#         log_attack(f"[!] Error saving to database: {e}")
#     finally:
#         conn.close()


# def fetch_rag_response(payload):

#     matched_commands = find_command_details(payload)

#     if not matched_commands:
#         log_attack(f"[!] No matching command found in '{payload}'.")
#         return ""

#     response_text = ""
#     for cmd in matched_commands:
#         command_name = cmd["command"]
#         log_attack(f"[*] Matched Command: {command_name}")


#         llm_prompt = (
#             f"The command '{command_name}' was identified in the given input.\n"
#             f"Original input: {payload}\n\n"
#             f"Command Summary: {cmd['summary']}\n\n"
#             f"Please generate the information that the flask server will return based on these contents. The specific content (including IP, file name, etc.) can be generated randomly."
#         )
        
#         detailed_response = generate_response(llm_prompt)
#         response_text += f"\n### Command: {command_name}\n{detailed_response}\n"

#     return response_text.strip()


# def get_response(payload):

#     payload_lower = payload.lower().strip()

#     if "\n" in payload_lower:
#         first_line = payload_lower.split("\n")[0]
#     else:
#         first_line = payload_lower

#     for key, response in STATIC_RESPONSES.items():
#         if first_line.startswith(key):
#             return response.encode("utf-8", errors="replace").decode("utf-8")

#     return fetch_rag_response(payload)


# app = Flask(__name__)


# @app.route("/", methods=["GET"])
# def index():
#     return "Request successful.", 200

# @app.route("/index.html", methods=["GET"])
# def index_html():
#     return "<html><body><h1>Index Page</h1></body></html>", 200

# @app.route("/about", methods=["GET"])
# def about():
#     return "This is the about page.", 200

# @app.route("/login", methods=["POST"])
# def login():
#     return "Access denied.", 403

# @app.route("/submit", methods=["POST"])
# def submit():
#     return "Submission received.", 200


# @app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
# def catch_all(path):
#     payload = f"{request.method.lower()} /{path}"

#     if request.data:
#         try:
#             data_decoded = request.data.decode("utf-8", errors="replace")
#         except Exception:
#             data_decoded = "[Invalid UTF-8 Data]"
#         payload += "\n" + data_decoded

#     log_attack(f"Request from {request.remote_addr}: {payload}")
#     response_text = get_response(payload)
    
#     threading.Thread(target=analyze_logs_and_define_strategy(payload), daemon=True).start()
    
#     return Response(response_text, mimetype="text/plain")


# if __name__ == "__main__":
#     init_database()
#     log_attack("[*] Flask Honeypot starting...")
#     app.run(host="0.0.0.0", port=8186)








# ssh
# import os
# import time
# import logging
# import threading
# import socket
# import paramiko
# from flask import Flask, Response
# from llm_response import generate_response
# from planning_agent import analyze_logs_and_define_strategy
# from search.huggingface_rag import fetch_data, find_command_details

# BASE_DIR = os.path.dirname(__file__)
# LOG_FILE = os.path.join(BASE_DIR, "honeypot.log")
# logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

# SERVER_KEY = paramiko.RSAKey.generate(2048)

# def log_attack(message):
#     log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}"
#     print(log_entry)
#     logging.info(log_entry)

# class FakeSSHServer(paramiko.ServerInterface):
#     def __init__(self):
#         self.event = threading.Event()

#     def check_auth_password(self, username, password):
#         log_attack(f"[*] Attacker entered username: {username}")
#         log_attack(f"[*] Attacker entered password: {password}")
#         return paramiko.AUTH_SUCCESSFUL

#     def check_channel_request(self, kind, chanid):
#         log_attack(f"[+] Channel request '{kind}'")
#         if kind == "session":
#             return paramiko.OPEN_SUCCEEDED
#         return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

#     def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
#         log_attack("[+] PTY request accepted")
#         return True

#     def check_channel_shell_request(self, channel):
#         log_attack("[+] Shell request accepted")
#         return True

# def fake_ssh_server():
#     HOST = "0.0.0.0"
#     PORT = 2222
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     server_socket.bind((HOST, PORT))
#     server_socket.listen(5)
#     log_attack("[*] Fake SSH server started on port 2222")

#     while True:
#         client, addr = server_socket.accept()
#         log_attack(f"[*] SSH Connection from {addr}")

#         transport = paramiko.Transport(client)
#         transport.add_server_key(SERVER_KEY)
#         server = FakeSSHServer()
#         transport.start_server(server=server)

#         chan = transport.accept(20)
#         if chan is None:
#             log_attack("[!] No channel opened.")
#             client.close()
#             continue

#         chan.send("\r\n")
#         chan.send("Welcome to Ubuntu 22.04 LTS (GNU/Linux 5.15.0-84-generic x86_64)\r\n")
#         chan.send(f"Last login: {time.strftime('%a %b %d %H:%M:%S %Y')} from {addr[0]}\r\n")
#         chan.send("$ ")

#         command_buffer = ""

#         while True:
#             try:
#                 data = chan.recv(1024)
#                 if not data:
#                     break

#                 command_part = data.decode("utf-8", errors="ignore")

#                 for char in command_part:
#                     chan.send(char)

#                     if char in ('\n', '\r'):
#                         command = command_buffer.strip()
#                         command_buffer = ""

#                         log_attack(f"[*] Attacker executed command: {command}")
#                         analyze_logs_and_define_strategy(command)  

#                         if command == "exit":
#                             chan.send("\nlogout\r\n")
#                             chan.close()
#                             break
#                         else:
#                             command_details = find_command_details(command)
#                             # print(f"command_details= {command_details}")
#                             llm_reply = generate_response(command_details)
#                             chan.send(f"\n{llm_reply}\r\n")

#                         chan.send("$ ")
#                     else:
#                         command_buffer += char

#             except Exception as e:
#                 log_attack(f"[!] SSH session error: {e}")
#                 break

#         chan.close()
#         client.close()
#         log_attack(f"[*] SSH Session closed for {addr}")

# ssh_thread = threading.Thread(target=fake_ssh_server, daemon=True)
# ssh_thread.start()

# app = Flask(__name__)

# @app.route("/", methods=["GET"])
# def index():
#     return "SSH Honeypot with LLM Response is running.", 200

# @app.route("/logs", methods=["GET"])
# def view_logs():
#     with open(LOG_FILE, "r") as f:
#         logs = f.readlines()
#     return Response("".join(logs), mimetype="text/plain")

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8186)



# 路径显示，错误指令识别
# import os
# import time
# import logging
# import threading
# import socket
# import paramiko
# from flask import Flask, Response
# from llm_response import generate_response 

# BASE_DIR = os.path.dirname(__file__)
# LOG_FILE = os.path.join(BASE_DIR, "honeypot.log")

# try:
#     if os.path.exists(LOG_FILE):
#         os.remove(LOG_FILE)
#         print(f"Removed old log file: {LOG_FILE}")
# except PermissionError:
#     print("Log file is locked by another process. Please close or stop any other program using it.")
# logging.basicConfig(
#     filename=LOG_FILE,
#     level=logging.INFO,
#     format="%(asctime)s - %(message)s",
#     filemode="w" 
# )
# SERVER_KEY = paramiko.RSAKey.generate(2048)
# USERNAME = "USbank"
# HOSTNAME = "Dataset_manage"

# def log_attack(message):
#     log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}"
#     print(log_entry)
#     logging.info(log_entry)

# def get_last_known_path():
#     if not os.path.exists(LOG_FILE):
#         return "~"
#     with open(LOG_FILE, "r") as f:
#         lines = f.readlines()
#     for line in reversed(lines):
#         if "CURRENT_PATH=" in line:
#             return line.strip().split("CURRENT_PATH=")[-1]
#     return "~"

# def format_prompt(path: str) -> str:
#     return f"{USERNAME}@{HOSTNAME}:{path}$ "

# class FakeSSHServer(paramiko.ServerInterface):
#     def __init__(self):
#         self.event = threading.Event()

#     def check_auth_password(self, username, password):
#         log_attack(f"[*] Attacker entered username: {username}")
#         log_attack(f"[*] Attacker entered password: {password}")
#         return paramiko.AUTH_SUCCESSFUL

#     def check_channel_request(self, kind, chanid):
#         log_attack(f"[+] Channel request '{kind}'")
#         if kind == "session":
#             return paramiko.OPEN_SUCCEEDED
#         return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

#     def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
#         log_attack("[+] PTY request accepted")
#         return True

#     def check_channel_shell_request(self, channel):
#         log_attack("[+] Shell request accepted")
#         return True

# def fake_ssh_server():
#     HOST = "0.0.0.0"
#     PORT = 2222
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     server_socket.bind((HOST, PORT))
#     server_socket.listen(5)
#     log_attack("[*] Fake SSH server started on port 2222")

#     while True:
#         client, addr = server_socket.accept()
#         log_attack(f"[*] SSH Connection from {addr}")

#         transport = paramiko.Transport(client)
#         transport.add_server_key(SERVER_KEY)
#         server = FakeSSHServer()
#         transport.start_server(server=server)

#         chan = transport.accept(20)
#         if chan is None:
#             log_attack("[!] No channel opened.")
#             client.close()
#             continue

#         current_path = get_last_known_path()

#         chan.send("\r\n")
#         chan.send("Welcome to Ubuntu 22.04 LTS (GNU/Linux 5.15.0-84-generic x86_64)\r\n")
#         chan.send(f"Last login: {time.strftime('%a %b %d %H:%M:%S %Y')} from {addr[0]}\r\n")
#         chan.send(format_prompt(current_path))

#         command_buffer = ""

#         while True:
#             try:
#                 data = chan.recv(1024)
#                 if not data:
#                     break

#                 command_part = data.decode("utf-8", errors="ignore")
#                 for char in command_part:
#                     chan.send(char)

#                     if char in ('\n', '\r'):
#                         chan.send("\r\n")

#                         command = command_buffer.strip()
#                         command_buffer = ""

#                         log_attack(f"[*] Attacker executed command: {command}")

                    
#                         if command == "exit":
#                             chan.send("logout\r\n")
#                             chan.close()
#                             break

                    
#                         elif command.startswith("cd "):
#                             new_dir = command[3:].strip()
#                             if new_dir == "..":
#                                 if current_path == "~":
#                                     pass
#                                 else:
#                                     current_path = os.path.dirname(current_path).rstrip("/")
#                                     if not current_path or current_path == "/":
#                                         current_path = "~"
#                             else:
#                                 if current_path == "~":
#                                     current_path = f"/{new_dir}"
#                                 else:
#                                     current_path = f"{current_path}/{new_dir}".replace("//", "/")

#                             log_attack(f"[PATH] CURRENT_PATH={current_path}")

#                             chan.send(format_prompt(current_path))

#                         else:
                            
#                             llm_reply = generate_response(command)
#                             chan.send(llm_reply)
#                             chan.send(format_prompt(current_path))

#                     else:
#                         command_buffer += char

#             except Exception as e:
#                 log_attack(f"[!] SSH session error: {e}")
#                 break

#         chan.close()
#         client.close()
#         log_attack(f"[*] SSH Session closed for {addr}")

# ssh_thread = threading.Thread(target=fake_ssh_server, daemon=True)
# ssh_thread.start()

# app = Flask(__name__)

# @app.route("/", methods=["GET"])
# def index():
#     return "SSH Honeypot with LLM Response is running.", 200

# @app.route("/logs", methods=["GET"])
# def view_logs():
#     with open(LOG_FILE, "r") as f:
#         logs = f.readlines()
#     return Response("".join(logs), mimetype="text/plain")

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8186)




import os
import time
import logging
import socket
import paramiko
import threading
from flask import Flask, Response
from llm_response import generate_response


BASE_DIR = os.path.dirname(__file__)
LOG_FILE = os.path.join(BASE_DIR, "honeypot.log")

try:
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
        print(f"Removed old log file: {LOG_FILE}")
except PermissionError:
    print("Log file is locked by another process. Please close or stop any other program using it.")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    filemode="w"
)

SERVER_KEY = paramiko.RSAKey.generate(2048)
USERNAME = "USbank"
HOSTNAME = "Dataset_manage"


def log_attack(message):
    log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    print(log_entry)
    logging.info(log_entry)


def get_last_known_path():
    if not os.path.exists(LOG_FILE):
        return "~"
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
    for line in reversed(lines):
        if "CURRENT_PATH=" in line:
            return line.strip().split("CURRENT_PATH=")[-1]
    return "~"

def format_prompt(path: str) -> str:
    return f"{USERNAME}@{HOSTNAME}:{path}$ "

class FakeSSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        log_attack(f"[*] Attacker entered username: {username}")
        log_attack(f"[*] Attacker entered password: {password}")
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_request(self, kind, chanid):
        log_attack(f"[+] Channel request '{kind}'")
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        log_attack("[+] PTY request accepted")
        return True

    def check_channel_shell_request(self, channel):
        log_attack("[+] Shell request accepted")
        return True


def fake_ssh_server():
    HOST = "0.0.0.0"
    PORT = 2222
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    log_attack("[*] Fake SSH server started on port 2222")

    while True:
        client, addr = server_socket.accept()
        log_attack(f"[*] SSH Connection from {addr}")

        try:
            transport = paramiko.Transport(client)
            transport.add_server_key(SERVER_KEY)
            server = FakeSSHServer()
            transport.start_server(server=server)

            chan = transport.accept(20)
            if chan is None:
                log_attack("[!] No channel opened.")
                client.close()
                continue

            current_path = get_last_known_path()

            chan.send("\r\n")
            chan.send("Welcome to Ubuntu 22.04 LTS (GNU/Linux 5.15.0-84-generic x86_64)\r\n")
            chan.send(f"Last login: {time.strftime('%a %b %d %H:%M:%S %Y')} from {addr[0]}\r\n")
            chan.send(format_prompt(current_path))

            command_buffer = ""

            while True:
                try:
                    data = chan.recv(1024)
                    if not data:
                        break

                    command_part = data.decode("utf-8", errors="ignore")
                    for char in command_part:
                        chan.send(char)

                        if char in ('\n', '\r'):
                            chan.send("\r\n")
                            command = command_buffer.strip()
                            command_buffer = ""

                            log_attack(f"[*] Attacker executed command: {command}")

                            if command == "exit":
                                chan.send("logout\r\n")
                                chan.close()
                                break

                            elif command.startswith("cd "):
                                new_dir = command[3:].strip()
                                if new_dir == "..":
                                    if current_path != "~":
                                        current_path = os.path.dirname(current_path).rstrip("/")
                                        if not current_path or current_path == "/":
                                            current_path = "~"
                                else:
                                    if current_path == "~":
                                        current_path = f"/{new_dir}"
                                    else:
                                        current_path = f"{current_path}/{new_dir}".replace("//", "/")

                                log_attack(f"[PATH] CURRENT_PATH={current_path}")
                                chan.send(format_prompt(current_path))
                            else:
                                llm_reply = generate_response(command)
                                chan.send(llm_reply)
                                chan.send(format_prompt(current_path))
                        else:
                            command_buffer += char

                except Exception as e:
                    log_attack(f"[!] SSH session error: {e}")
                    break

            chan.close()
            client.close()
            log_attack(f"[*] SSH Session closed for {addr}")

        except Exception as e:
            log_attack(f"[!] Top-level connection error: {e}")
            try:
                client.close()
            except:
                pass

# ========== 启动 SSH Server ==========
ssh_thread = threading.Thread(target=fake_ssh_server, daemon=True)
ssh_thread.start()

# ========== Flask Web 接口 ==========
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "SSH Honeypot with LLM Response is running.", 200

@app.route("/logs", methods=["GET"])
def view_logs():
    with open(LOG_FILE, "r") as f:
        logs = f.readlines()
    return Response("".join(logs), mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8186)
