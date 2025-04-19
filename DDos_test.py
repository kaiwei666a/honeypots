#!/usr/bin/env python3
import paramiko
import time

def ssh_connection_test(
    hostname="localhost",
    port=2222,
    username="user",
    password="",
    connection_count=10,
    delay=0.5
):
    """
    反复尝试对指定的 SSH 服务器进行连接，以测试其对大量或频繁连接的处理能力。
    
    :param hostname:       目标主机名/IP（默认 "localhost"）
    :param port:           SSH 端口（默认 2222）
    :param username:       SSH 用户名
    :param password:       SSH 密码，若使用密钥认证则留空并设置 key 文件
    :param connection_count: 需要进行的连接次数
    :param delay:          每次连接之间的延时，单位：秒
    """
    # 创建一个SSH客户端对象
    client = paramiko.SSHClient()
    
    # 若目标是测试环境或 Honeypot，可避免在 known_hosts 中校验
    # 不建议在生产环境下使用 AutoAddPolicy
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for i in range(connection_count):
        try:
            # 建立连接
            print(f"[{i+1}/{connection_count}] Attempting to connect to {hostname}:{port}...")
            client.connect(
                hostname=hostname,
                port=port,
                username=username,
                password=password,
                look_for_keys=False,
                allow_agent=False,
                timeout=5  # 连接超时时间，可根据需要调整
            )
            
            # 如果连接成功，可在此处执行命令或其他操作
            stdin, stdout, stderr = client.exec_command("echo 'Hello from test script'")
            result = stdout.read().decode().strip()
            print(f"SSH Command Output: {result}")
            
        except paramiko.AuthenticationException as e:
            print("[!] Authentication failed:", str(e))
        except paramiko.SSHException as e:
            print("[!] SSH error occurred:", str(e))
        except Exception as e:
            print("[!] General error occurred:", str(e))
        finally:
            # 关闭连接
            client.close()
        
        # 在下次连接前的延时，避免太快造成网络或系统过载
        time.sleep(delay)

if __name__ == "__main__":
    # 使用示例：按需修改测试参数
    hostname = "localhost"
    port = 2222
    username = "user"
    password = "454"          # 如果 Honeypot 不要求密码可保持空
    connection_count = 10   # 连接次数
    delay = 0.5            # 每次连接之间的延迟，避免过度刷屏或过载

    ssh_connection_test(
        hostname=hostname,
        port=port,
        username=username,
        password=password,
        connection_count=connection_count,
        delay=delay
    )
