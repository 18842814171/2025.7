from openai import OpenAI
import pandas as pd
import base64
API_KEY="sk-6abec274d9f14e7d954603d3884e99ef"
#  base 64 编码格式
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_response(image_path,questions):
    base64_image = encode_image(image_path)
    client = OpenAI(
        api_key=API_KEY,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen-vl-plus",
        messages=[ {
        "role": "system",
        "content": "请100字以内回答所有问题，保持回答简短直接。"
    },
            {
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": questions,
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                  }
                }
              ]
            }
          ]
          # stream=True,
          # stream_options={"include_usage":True}
        )
    #for chunk in completion:
    print(completion)

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
    image_urls = df['image_id'].dropna().tolist()   # 改列名
    
    # 确保两个列表长度一致
    min_length = min(len(questions), len(image_urls))
    questions = questions[:min_length]
    image_urls = image_urls[:min_length]
    
    return questions, image_urls

if __name__=='__main__':
    QUESTIONS, IMAGE_URLS = read_table('D:/作业/其他/测试代码/0_output.xlsx',start_row=0, end_row=4)
    for i, (question, img_url) in enumerate(zip(QUESTIONS, IMAGE_URLS)):
        get_response(img_url,question)
