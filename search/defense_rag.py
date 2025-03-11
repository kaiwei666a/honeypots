import openai
import requests
from bs4 import BeautifulSoup
import os

def fetch_mitre_defense_methods(url):
    response = requests.get(url)
    if response.status_code != 200:
        return "Error: Unable to fetch data from MITRE ATT&CK."
    
    soup = BeautifulSoup(response.text, 'html.parser')
    defense_methods = []
    
    for section in soup.find_all("h2"):
        if "Mitigations" in section.text:
            mitigations = section.find_next("ul")
            if mitigations:
                defense_methods = [li.text.strip() for li in mitigations.find_all("li")]
    
    return "\n".join(defense_methods) if defense_methods else "No defense methods found."

def generate_ssh_protection_code(defense_requirements):
    prompt = f"""
    Based on the following security requirements, generate a Python script that enhances SSH security:
    {defense_requirements}
    Ensure best practices are followed.
    """
    
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a cybersecurity expert."},
            {"role": "user", "content": prompt}
        ]
    )
    
    response_data = response.model_dump()
    ssh_protection_code = response_data.get("choices", [{}])[0].get("message", {}).get("content", "Error: No content generated.")
    return ssh_protection_code

if __name__ == "__main__":
    mitre_url = "https://attack.mitre.org/techniques/T1059/006/"
    defense_requirements = fetch_mitre_defense_methods(mitre_url)
    
    code = generate_ssh_protection_code(defense_requirements)
    print("Generated SSH Protection Code:")
    print(code)