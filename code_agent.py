import openai

def generate_code(prompt, model="gpt-4o-mini", temperature=0.7, max_tokens=1000):
    """
    调用 OpenAI API 生成代码。
    
    :param prompt: 用户输入的提示
    :param model: 使用的 LLM 模型
    :param temperature: 生成的随机性（0-1 之间）
    :param max_tokens: 生成文本的最大长度
    :return: 生成的代码
    """
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": "You are a helpful coding assistant."},
                  {"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response["choices"][0]["message"]["content"]

if __name__ == "__main__":
    user_prompt = "写一个Python函数计算斐波那契数列"
    generated_code = generate_code(user_prompt)
    print("code:\n", generated_code)