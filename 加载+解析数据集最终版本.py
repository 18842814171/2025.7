from datasets import load_dataset
import os
import json

# 加载数据集
dataset = load_dataset("crag-mm-2025/crag-mm-multi-turn-public", revision="v0.1.1")

# 基础输出目录
base_output_dir = r"D:/作业/程序设计/小组作业/crag-mm-2025数据集/multi-turn"
os.makedirs(base_output_dir, exist_ok=True)

# 图片子目录
image_dir = os.path.join(base_output_dir, "picture")
os.makedirs(image_dir, exist_ok=True)

# 处理数据
split_to_use = "validation"
samples_per_file = 100  # 每个文件保存100条会话
num_files = 5          # 共生成5个文件
total_samples = len(dataset[split_to_use])

# 创建映射文件
mapping_file = os.path.join(base_output_dir, "mapping_index.csv")
with open(mapping_file, 'w', encoding='utf-8') as map_f:
    map_f.write("image_name,file_name,item_index,session_id\n")

for i in range(num_files):
    start_idx = i * samples_per_file
    end_idx = min((i + 1) * samples_per_file, total_samples)
    output_file = os.path.join(base_output_dir, f"conversations_{i}.json")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for w in range(start_idx, end_idx):
            ex = dataset[split_to_use][w]
            if not isinstance(ex, dict):
                continue
                
            # 构建数据记录
            record = {
                **{k: v for k, v in ex.items() if k != 'image'},
                "conversation_index": w,
                "image_file": None
            }
            
            # 保存图片
            if 'image' in ex and ex['image']:
                img_name = f"img_{w}.jpg"
                ex['image'].save(os.path.join(image_dir, img_name))
                record["image_file"] = img_name
                
                # 写入映射关系（单独打开映射文件避免冲突）
                with open(mapping_file, 'a', encoding='utf-8') as map_f:
                    map_f.write(f"{img_name},{os.path.basename(output_file)},{w},{ex['session_id']}\n")
            
            # 写入JSON行
            json.dump(record, f, ensure_ascii=False)
            f.write('\n')
    
    print(f"Saved {output_file} (items {start_idx}-{end_idx-1})")