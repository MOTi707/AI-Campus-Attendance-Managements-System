"""测试 OpenAI API 调用"""
from openai import OpenAI

# API 配置
API_KEY = 'sk-rpuequlhparhcmoewdrfixlrjmeywjxwxskwebcbzkhjnxtd'
BASE_URL = 'https://api.siliconflow.cn/v1'
MODEL = 'deepseek-ai/DeepSeek-V3'

print('=' * 50)
print('测试 OpenAI SDK 调用')
print('=' * 50)

try:
    # 初始化客户端
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    print('✅ 客户端初始化成功')
    
    # 调用 API
    print(f'📡 调用 {MODEL}...')
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {'role': 'system', 'content': '你是一个有帮助的助手。'},
            {'role': 'user', 'content': '你好，请用一句话介绍你自己'}
        ],
        temperature=0.7,
        max_tokens=100,
        stream=False
    )
    
    content = response.choices[0].message.content
    print('✅ API 调用成功！')
    print(f'📝 AI 回复: {content}')
    print(f'📊 回复长度: {len(content)} 字符')
    
except Exception as e:
    print(f'❌ 错误: {str(e)}')
    import traceback
    traceback.print_exc()
