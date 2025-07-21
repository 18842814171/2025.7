import base64
import pandas as pd
HUNYUAN_API_KEY="sk-qidIjiH5r4e8U0ivA5VQyvpsZgJGa7zG13Fs0HrQby7zNY7C"
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
import time
import os
from openai import OpenAI

# 构造 client
def batch_query(questions, image_urls):
    client = OpenAI(
        api_key=HUNYUAN_API_KEY, # 混元 APIKey
        base_url="https://api.hunyuan.cloud.tencent.com/v1", # 混元 endpoint
    )
    results = []
    for i, (question, img_url) in enumerate(zip(questions, image_urls)):
        try:
            base64_image = encode_image(img_url)
            completion = client.chat.completions.create(
                model="hunyuan-vision",
                messages=[{
                        "role": "system",
                        "content": "请100字以内回答所有问题，保持回答简短直接。"
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": question},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    },
                ],
                max_tokens=100
            )
         # 立即打印当前问题的答案
            answer = completion.choices[0].message.content
            print(f"\n问题 {i+1}: {question}\n答案: {answer}")  # 新增实时输出
            
            result = {"question": question, "answer": answer}
            time.sleep(5)
            
        except Exception as e:
            print(f"\n问题 {i+1}: {question}\n错误: {str(e)}")  # 错误也实时输出
            result = {"question": question, "error": str(e)}
            time.sleep(5)
            
        results.append(result)
    
    return results
         
def read_table(file_path, start_row=0, end_row=None):
    """
    从Excel表格文件中读取指定行的问题和图片URL
    参数:
        file_path: Excel表格文件路径
        start_row: 起始行索引（包含，从0开始计数），默认为0
        end_row: 结束行索引（包含，从0开始计数），默认为None表示读取到最后一行
    返回:
        questions: 问题列表（来自turns列）
        image_urls: 图片URL列表（来自image_url列）
    """
    # 读取Excel文件
    df = pd.read_excel(file_path)
    
    # 筛选指定行范围的数据
    if end_row is not None:
        df = df.iloc[start_row:end_row+1]  # iloc是左闭右开，所以end_row+1
    else:
        df = df.iloc[start_row:]
    
    # 提取指定列数据并处理缺失值
    questions = df['turns'].dropna().tolist()
    image_urls = df['img_id'].dropna().tolist()   # 改列名
    
    # 确保两个列表长度一致
    min_length = min(len(questions), len(image_urls))
    questions = questions[:min_length]
    image_urls = image_urls[:min_length]
    
    return questions, image_urls

if __name__ == '__main__':
    IMAGE_FOLDER = "D:/作业/程序设计/小组作业/crag-mm-2025数据集/multi-turn-7.14/picture/"  # 图片文件夹根目录
    
    QUESTIONS, IMAGE_IDS = read_table('D:/作业/程序设计/小组作业/crag-mm-2025数据集/multi-turn-7.14/问题.xlsx',start_row=5,end_row=29) 
    # 拼接完整图片路径
    IMAGE_URLS = [IMAGE_FOLDER + img_id for img_id in IMAGE_IDS]
    
    answers = batch_query(QUESTIONS, IMAGE_URLS)
    
    with open("HUNYUAN7.18.txt", "a", encoding="utf-8") as f:
        for i, ans in enumerate(answers):
            output = f"\n问题 {i+1}:\nQ: {ans['question']}\n"
            output += f"A: {ans['answer']}\n" if "answer" in ans else f"错误: {ans['error']}\n"
            #print(output)
            f.write(output)