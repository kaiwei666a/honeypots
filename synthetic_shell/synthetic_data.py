import os
import json
from typing import Dict, Any
import openai

class ShellCommandGenerator:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def load_example(self) -> str:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        example_path = os.path.join(script_dir, "shell_example.json")
        try:
            with open(example_path, "r", encoding="utf-8") as f:
                example_json = json.load(f)
            return json.dumps(example_json, indent=4)
        except Exception as e:
            print("Error loading shell_example.json:", str(e))
            return ""

    def generate_command(self, instruction: str) -> Dict[str, Any]:
        try:
            example_text = self.load_example()

            prompt = f"""
                        You are a helpful assistant skilled in writing Linux bash shell commands.

                        You have access to a wide range of shell command categories. For the given natural language instruction, generate exactly 10 relevant bash commands across all of the categories listed below.

                        For each command:
                        - If the instruction is valid, provide a realistic shell command with sample output as feedback.
                        - If the instruction is invalid, ambiguous, misspelled, or resembles an incorrect shell command, simulate what the Linux shell would realistically respond with, such as:
                        - `command not found`
                        - `bash: syntax error near unexpected token`
                        - `No such file or directory`
                        - Suggestions like “Did you mean ...?”

                        Also, for incorrect input, **do not fix the command** — simply reflect how a real bash shell would respond to the input.

                        Use these categories to guide your selection of commands:

                            1. File and directory operations  
                            - Examples: ls, cp, mv, rm, find, du, df, tree.
                            2. Text processing  
                            - Examples: grep, awk, sed, cut, sort, uniq, tr, wc.
                            3. Process and resource monitoring  
                            - Examples: top, htop, ps, kill, vmstat, iostat, free, uptime.
                            4. User and permission management  
                            - Examples: chmod, chown, useradd, passwd, groups, whoami, sudo.
                            5. Network and port operations  
                            - Examples: ping, curl, wget, netstat, ss, ifconfig, dig, traceroute, nmap.
                            6. Development tools  
                            - Examples: gcc, make, python, node, javac, git, docker.
                            7. Package management  
                            - Examples: apt, yum, snap, brew, dpkg, rpm, pip, npm.
                            8. Security and encryption  
                            - Examples: ssh, ssh-keygen, gpg, openssl, chmod, firewall-cmd, ufw.
                            9. System automation and special shell tricks  
                            - Examples: cron, at, alias, nohup, screen, tmux, xargs, watch, &&, ||.

                        Use realistic filenames or directory names in commands and outputs, such as:
                        - ssh_keys.pub
                        - config.yml
                        - secrets.env
                        - finance_backup_2023.tar.gz

                        Format your output strictly as JSON using the following structure (no markdown, no triple backticks):

                        {{
                                                    "commands": [
                                                        {{
                                                        "command": "<bash command>",
                                                        "feedback": "<sample output of the command>"
                                                        }},
                                                        ...
                                                    ]
                                                    }}

                        Guidelines:
                        - Output exactly 10 command objects.
                        - At least 2 of them should reflect how the shell responds to invalid or malformed commands.
                        - Do not wrap your output in any markdown or commentary.
                        - Do not include internal reasoning.


                        """

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant skilled in writing Linux bash shell commands."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2
            )
            print(response)
            answer = response.choices[0].message.content.strip()
            print(answer)
            if answer.startswith("```") and answer.endswith("```"):
                answer = answer[3:-3].strip()
            result = json.loads(answer)
            return {"success": True, "commands": result.get("commands", [])}
        except Exception as e:
            return {"success": False, "error": str(e)}

if __name__ == "__main__":
    generator = ShellCommandGenerator()
    instruction = "List all .txt files in the current directory and count the total number of lines"
    result = generator.generate_command(instruction)
    if result["success"]:
        commands_list = result["commands"]
    else:
        commands_list = [{"error": result["error"]}]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_filename = os.path.join(script_dir, "shellcommand.json")
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(commands_list, f, indent=4, ensure_ascii=False)
        print(f"Results saved to {output_filename}")
    except Exception as e:
        print("Error saving results:", str(e))







    # You are a helpful assistant skilled in writing Linux bash shell commands.

    #                         You have access to a wide range of shell command categories. For the given natural language instruction, generate exactly 10 relevant bash commands across all of the categories listed below.

    #                         Each command must be accompanied by realistic-looking feedback, as if the command had actually been run. The feedback should simulate real output — including directory structures, file listings, logs, results, etc.

    #                         Additionally, when referencing files or directories in the commands or their outputs, use **random but realistic and sensitive-looking names**, such as:
    #                         - config.yaml
    #                         - ssh_keys.pub
    #                         - finance_backup_2023.tar.gz
    #                         - confidential_notes.txt
    #                         - secrets.env
    #                         - db_dump.sql
    #                         - user_data.csv
    #                         - system.log

    #                         This makes the command output look more authentic and practical.

    #                         Your goal is to maximize coverage across categories, not just provide the single most obvious command.

    #                         Use these categories as your guide:

    #                         1. File and directory operations  
    #                         - Examples: ls, cp, mv, rm, find, du, df, tree.
    #                         2. Text processing  
    #                         - Examples: grep, awk, sed, cut, sort, uniq, tr, wc.
    #                         3. Process and resource monitoring  
    #                         - Examples: top, htop, ps, kill, vmstat, iostat, free, uptime.
    #                         4. User and permission management  
    #                         - Examples: chmod, chown, useradd, passwd, groups, whoami, sudo.
    #                         5. Network and port operations  
    #                         - Examples: ping, curl, wget, netstat, ss, ifconfig, dig, traceroute, nmap.
    #                         6. Development tools  
    #                         - Examples: gcc, make, python, node, javac, git, docker.
    #                         7. Package management  
    #                         - Examples: apt, yum, snap, brew, dpkg, rpm, pip, npm.
    #                         8. Security and encryption  
    #                         - Examples: ssh, ssh-keygen, gpg, openssl, chmod, firewall-cmd, ufw.
    #                         9. System automation and special shell tricks  
    #                         - Examples: cron, at, alias, nohup, screen, tmux, xargs, watch, &&, ||.

    #                         Format your output strictly as JSON using the following structure and without any markdown formatting (do not include triple backticks):

    #                         {{
    #                             "commands": [
    #                                 {{
    #                                 "command": "<bash command>",
    #                                 "feedback": "<sample output of the command>"
    #                                 }},
    #                                 ...
    #                             ]
    #                             }}

    #                         Guidelines:
    #                         - Output exactly 10 command objects.
    #                         - Use realistic, varied, and sensitive-looking filenames in commands and output.
    #                         - Do not include internal reasoning or markdown formatting in the final output.

    #                         Instruction: {instruction}




# 包含错误指令的响应

# You are a helpful assistant skilled in writing Linux bash shell commands.

# You have access to a wide range of shell command categories. For the given natural language instruction, generate exactly 10 relevant bash commands across all of the categories listed below.

# For each command:
# - If the instruction is valid, provide a realistic shell command with sample output as feedback.
# - If the instruction is invalid, ambiguous, misspelled, or resembles an incorrect shell command, simulate what the Linux shell would realistically respond with, such as:
#   - `command not found`
#   - `bash: syntax error near unexpected token`
#   - `No such file or directory`
#   - Suggestions like “Did you mean ...?”

# Also, for incorrect input, **do not fix the command** — simply reflect how a real bash shell would respond to the input.

# Use these categories to guide your selection of commands:

# 1. File and directory operations  
# 2. Text processing  
# 3. Process and resource monitoring  
# 4. User and permission management  
# 5. Network and port operations  
# 6. Development tools  
# 7. Package management  
# 8. Security and encryption  
# 9. System automation and shell tricks  

# Use realistic filenames or directory names in commands and outputs, such as:
# - ssh_keys.pub
# - config.yml
# - secrets.env
# - finance_backup_2023.tar.gz

# Format your output strictly as JSON using the following structure (no markdown, no triple backticks):

# {{
#                             "commands": [
#                                 {{
#                                 "command": "<bash command>",
#                                 "feedback": "<sample output of the command>"
#                                 }},
#                                 ...
#                             ]
#                             }}

# Guidelines:
# - Output exactly 10 command objects.
# - At least 2 of them should reflect how the shell responds to invalid or malformed commands.
# - Do not wrap your output in any markdown or commentary.
# - Do not include internal reasoning.




