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


    client = paramiko.SSHClient()
    

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for i in range(connection_count):
        try:

            print(f"[{i+1}/{connection_count}] Attempting to connect to {hostname}:{port}...")
            client.connect(
                hostname=hostname,
                port=port,
                username=username,
                password=password,
                look_for_keys=False,
                allow_agent=False,
                timeout=5 
            )
            

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
          
            client.close()
        
   
        time.sleep(delay)

if __name__ == "__main__":

    hostname = "localhost"
    port = 2222
    username = "user"
    password = "454"         
    connection_count = 10 
    delay = 0.5          

    ssh_connection_test(
        hostname=hostname,
        port=port,
        username=username,
        password=password,
        connection_count=connection_count,
        delay=delay
    )
