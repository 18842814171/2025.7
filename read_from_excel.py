import pandas as pd

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
    image_urls = df['image_url'].dropna().tolist()
    
    # 确保两个列表长度一致
    min_length = min(len(questions), len(image_urls))
    questions = questions[:min_length]
    image_urls = image_urls[:min_length]
    
    return questions, image_urls



# 执行流程
if __name__ == "__main__":
        QUESTIONS, IMAGE_URLS = read_table('D:/作业/其他/测试代码/0_output.xlsx',start_row=8, end_row=18)
        print(f"成功读取 {len(QUESTIONS)} 个问题和 {len(IMAGE_URLS)} 个图片URL")
        print("问题列表:", QUESTIONS)
        print("图片URL列表:", IMAGE_URLS)
       