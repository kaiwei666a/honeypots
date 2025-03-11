import openai
import os

def generate_ssh_protection_code(defense_requirements):
    prompt = f"""
    Based on the following security requirements, generate a Python script that enhances SSH security:
    {defense_requirements}
    Ensure best practices are followed.
    """
    
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a cybersecurity expert."},
            {"role": "user", "content": prompt}
        ]
    )
    
    response_data = response.model_dump()
    ssh_protection_code = response_data.get("choices", [{}])[0].get("message", {}).get("content", "Error: No content generated.")
    return ssh_protection_code

if __name__ == "__main__":
    with open("define_log.txt", "r") as file:
        defense_requirements = file.read().strip()
    
    code = generate_ssh_protection_code(defense_requirements)
    print("Generated SSH Protection Code:")
    print(code)
