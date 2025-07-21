import json

def extract_and_combine_text_fields(file_content):
    questions = file_content.split('\n\n\n ')[1:]  # 分割每个问题
    results = {}
    
    for i, question in enumerate(questions, 1):
        # 提取问题部分的所有event:message块
        message_blocks = [block for block in question.split('\n') if block.startswith('data:')]
        combined_text = ""
        
        for block in message_blocks:
            try:
                data = json.loads(block[5:])  # 去掉'data:'前缀
                # 检查是否有content字段且是列表
                if 'data' in data and 'message' in data['data'] and 'content' in data['data']['message']:
                    content = data['data']['message']['content']
                    if isinstance(content, list):
                        for item in content:
                            if isinstance(item, dict) and 'data' in item and isinstance(item['data'], dict) and 'text' in item['data']:
                                combined_text += item['data']['text']
            except json.JSONDecodeError:
                continue
        
        results[f" {i}"] = combined_text
    
    return results

# 从文件中读取内容
with open('output2.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# 提取并合并text字段
combined_texts = extract_and_combine_text_fields(content)

with open('wenxin_output.txt', 'w', encoding='utf-8') as f:
    for question, text in combined_texts.items():
        f.write(f"{question}: {text}\n\n")