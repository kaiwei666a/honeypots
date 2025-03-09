import paramiko
import socket
import threading
import time

LOG_FILE = "ssh_honeypot.log"


HOST_KEY = paramiko.RSAKey.generate(2048)


class FakeSSHServer(paramiko.ServerInterface):
    def __init__(self, client_ip):
        self.client_ip = client_ip

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        log_message = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] SSH Login attempt from {self.client_ip} | Username: {username} | Password: {password}\n"
        print(log_message)
        with open(LOG_FILE, "a", encoding="utf-8") as log_file:
            log_file.write(log_message)
        return paramiko.AUTH_SUCCESSFUL 


def handle_ssh_connection(client, addr):
    try:
        transport = paramiko.Transport(client)
        transport.add_server_key(HOST_KEY)
        server = FakeSSHServer(addr[0])
        transport.start_server(server=server)

        channel = transport.accept(20) 
        if channel is None:
            return

        channel.send("Welcome to Ubuntu 20.04 LTS\n$ ")
        while True:
            command = channel.recv(1024).decode("utf-8", errors="ignore").strip()
            if not command:
                break
            log_message = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {addr[0]} executed: {command}\n"
            print(log_message)
            with open(LOG_FILE, "a", encoding="utf-8") as log_file:
                log_file.write(log_message)
            channel.send("bash: command not found\n$ ")

    except Exception as e:
        print(f"[*] Error with {addr[0]}: {e}")
    finally:
        client.close()

def start_ssh_honeypot():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 22))
    server.listen(5)
    print("[*] SSH Honeypot running on port 22...")

    while True:
        try:
            client, addr = server.accept()
            threading.Thread(target=handle_ssh_connection, args=(client, addr)).start()
        except KeyboardInterrupt:
            print("\n[*] Shutting down honeypot.")
            server.close()
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    start_ssh_honeypot()
