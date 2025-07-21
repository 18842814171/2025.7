import requests
import base64
import os
import json
import pandas as pd
import glob
import time

def get_access_token(api_key, api_secret):
    url = "https://chatglm.cn/chatglm/assistant-api/v1/get_token"
    data = {"api_key": api_key, "api_secret": api_secret}
    response = requests.post(url, json=data)
    return response.json()["result"]["access_token"]

def upload_image(access_token, image_path):
    url = "https://chatglm.cn/chatglm/assistant-api/v1/file_upload"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    with open(image_path, "rb") as f:
        files = {"file": (os.path.basename(image_path), f)}
        response = requests.post(url, headers=headers, files=files)
    
    response_data = response.json()
    if "result" in response_data and "file_id" in response_data["result"]:
        return response_data["result"]["file_id"]
    else:
        raise ValueError(f"上传失败: {response_data}")

def send_message_with_image(assistant_id, access_token, prompt, file_id, output_file):
    url = "https://chatglm.cn/chatglm/assistant-api/v1/stream"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "assistant_id": assistant_id,
        "prompt": prompt,
        "file_list": [{"file_id": file_id}]
    }
    
    last_text = None
    with requests.post(url, json=data, headers=headers, stream=True) as response:
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")
                    if decoded_line.startswith("data: "):
                        try:
                            json_line = json.loads(decoded_line[6:])
                            if json_line.get("message", {}).get("content", {}).get("type") == "text":
                                last_text = json_line["message"]["content"]["text"]
                                print(f"答案: {last_text}")  # 控制台输出答案
                        except json.JSONDecodeError:
                            pass
    
    # 写入文件
    with open(output_file, "a", encoding="utf-8") as f:
        if last_text:
            f.write(f"问题: {prompt}\n答案: {last_text}\n\n")
        else:
            f.write(f"问题: {prompt}\n答案: 无有效响应\n\n")

if __name__ == "__main__":
    # 配置参数
    api_key = 'ea2976c773218dd7'
    api_secret = 'f731ca29401f88bcff9d4710599138d2'
    assistant_id = "68773ad4dd38bc80642c9c35"
    image_folder = "D:/作业/程序设计/小组作业/crag-mm-2025数据集/multi-turn-7.14/picture/"
    output_file = "answers.txt"
    
    # 初始化输出文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("")
    
    # 读取表格
    df = pd.read_excel("D:/作业/程序设计/小组作业/crag-mm-2025数据集/multi-turn-7.14/问题.xlsx")
    prompts = df['turns'].tolist()
    image_ids = df['img_id'].tolist()
    
    # 获取access_token
    access_token = get_access_token(api_key, api_secret)
    
    # 处理每个问题
    for i, (prompt, img_id) in enumerate(zip(prompts, image_ids)):
        img_path = os.path.join(image_folder, img_id)
        print(f"\n处理第 {i+1} 个问题: {prompt}")
        
        try:
            file_id = upload_image(access_token, img_path)
            send_message_with_image(assistant_id, access_token, prompt, file_id, output_file)
            time.sleep(5)  # 每次请求间隔5秒
        except Exception as e:
            print(f"处理失败: {str(e)}")
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"问题: {prompt}\n错误: {str(e)}\n\n")
            time.sleep(5)