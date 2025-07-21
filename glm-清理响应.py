import json
def clean_response(input_file,output_file):
    # 读取文件内容
    with open(input_file, "r", encoding="utf-8") as file:
        content = file.read()

    # 分割成多行，每行是一个 JSON 对象
    lines = content.strip().split("\ndata: ")

    # 提取 text 字段
    with open(output_file, "w", encoding="utf-8") as out_put:
        for line in lines[1:]:  # 跳过第一行（空或标题）
            try:
                data = json.loads(line)
                text = data["message"]["content"]["text"]
                out_put.write(text + "\n")  # 每条 text 占一行
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
            except KeyError as e:
                print(f"Missing key: {e}")
    print("Texts have been saved to extracted_texts.txt")

input_file=r"glm/1response.txt"
output_file=r"glm/1cleaned.txt"
clean_response(input_file,output_file)