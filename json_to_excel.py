import pandas as pd
import json
import os
import re

def extract_img_id(image_file):
    """直接从image_file字段提取图片名称"""
    if not image_file:
        return "unknown.jpg"
    # 简单返回image_file的值，因为它已经是文件名
    return image_file

# 使用原始字符串处理Windows路径
file_path = r"D:/作业/程序设计/小组作业/crag-mm-2025数据集/multi-turn-7.14/conversations/conversations_4.json"

# 读取JSON文件
data_list = []
with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:  # 跳过空行
            try:
                data = json.loads(line)
                # 提取数据
                img_id = extract_img_id(data.get("image_file", ""))
                turns = " ||| ".join([turn["query"] for turn in data["turns"]])
                answers = " ||| ".join([answer["ans_full"] for answer in data["answers"]])
                
                data_list.append({
                    "img_id": img_id,
                    "turns": turns,
                    "answers": answers
                })
            except json.JSONDecodeError as e:
                print(f"JSON解析错误（跳过该行）: {e}")
            except KeyError as e:
                print(f"缺少必要字段 {e}（跳过该行）")

# 创建DataFrame并保存为Excel
if data_list:
    df = pd.DataFrame(data_list)
    
    # 在原始文件同目录下保存结果
    output_path = "4_output.xlsx"
    df.to_excel(output_path, index=False, engine="openpyxl")
    print(f"成功处理 {len(df)} 条数据，已保存到: {output_path}")
    
    # 打印前3行作为预览
    print("\n数据预览:")
    print(df.head(3))
else:
    print("未找到有效数据！")