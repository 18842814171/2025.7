import requests
import uuid
import time

# 配置参数
API_URL = "https://agent-proxy-ws.baidu.com/agent/call/conversation"
HEADERS = {
    "Content-Type": "application/json",
    "Cookie": "BIDUPSID=E42263344D69156A8B4332C5D82C4EC2;PSTM=1750499427;H_PS_PSSID=60276_62325_63147_63326_63275_63881_63911_63903_63947_63995_64008_64016_64027_64058_64055_64050_64038_64089_64085_64092;BAIDUID=E42263344D69156A8B4332C5D82C4EC2FG=1;H_WISE_SIDS=60276_62325_63147_63326_63275_63881_63911_63903_63947_63995_64008_64016_64027_64058_64055_64050_64038_64089_64085_64092;MAWEBCUID=web_yPxuEzOSMNKiOkRWzUOPBmdoqiCrZuJPhpSMXvHDVEKMetSnvd;BDUSS=ItVkRsSjRwSkozaW91ZzIwckRYdDJxNXRLY0VMWGVxQm15Y0N2cH5wa0F-SmRvRVFBQUA3F8A630C64834BD6D0;ZFY=Md9V7eay3ulO2ySktPjZF26vCTy82mA2UVdvunlMvT0C;delPer=0;PSINO=1;RT=z=1dm=baidu.comsi=03d8a0ac-d380-4b1a-85e6-61f74fba989ess=md8iiyjksl=5tt=6tdbcn=https3A2F2Ffclog.baidu.com2Flog2Fweirwood3Ftype3Dperfld=cbo;__bid_n=197e901046a6864c426a5f;ab_sr=1.0.1_NzQxZTZjYTM0OWMyZTAyNTQ1MWM5MzYxMTMzZDQxODg1MzQ0NDI3MDMzZjk2MzJlNWYwZjVhNzMwOWMwYWFhOTNmZjA3NTI3NzExNzRhMmVlM2RmMGExNjU5YTM1MTRiNGMyMjAyMjg4MDc4NjcwOTc3YjY4YjNmYzRhYWZjZjRlMjRmNzUzM2IyNTg5NTI1MTI3N2ZjYTFkMGFlMTRmMg==",
    "Referer": "https://smartapps.baidu.com/",
    "Origin": "https://smartapps.baidu.com",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0"
}
APP_ID = "OLdnBMrbRvMPaYibFiXyPlfPGKWjgabD"
sessionId= "1752824617319948608"
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




# 批量发送问题+图片
def batch_query(questions, image_urls, sessionId):
    results = []
    for i, (question, img_url) in enumerate(zip(questions, image_urls)):
        traceid = uuid.uuid4().hex  # 每次请求唯一traceid
        data = {
            "appId": APP_ID,
            "versionCode":4,"versionType":"online",
            "sessionId": sessionId,
            "content": {
                "query": {
                    "type": "multimodal",
                    "value": [
                        {"type": "text", "value": {"showText": question}},
                        {"type": "image", "value": {"imageUrl": img_url,"imageType":"jpg",
                                  "imageSize":0}}
                    ]
                }
            },
            "regenerateInfo":{"isRegenerated":False},
            "inputMethod":"keyboard",
            "querySource":"input_box",
            "log":{"channel_id":"3621000000000000","lid":"","tplname":"","srcid":"","order":"","csaitab_lid":""},
            "chatRound":1,
            "transData":[
            {"from":"agent_proxy","type":"json","key":"channel","value":"3621000000000000"},
             {"from":"agent_proxy","type":"json","key":"action","value":"[\"\"]"}
             ]
        }
        try:
            response = requests.post(
                f"{API_URL}?traceld={traceid}",
                json=data,
                headers=HEADERS,
                timeout=10
            )
            result = {
                "status_code": response.status_code,
                "raw_response": response.text,  # 原始响应文本
                #"parsed_response": response.json()  # 解析后的JSON（可能失败）
            }
            results.append(result)
            
        except Exception as e:
            # 如果解析JSON失败，仍保留原始响应文本
            error_result = {
                "error": str(e),
                "raw_response": getattr(response, 'text', '无响应'),  # 确保获取原始文本
                "status_code": getattr(response, 'status_code', '无状态码')
            }
            results.append(error_result)
            print(f"请求 {i+1} 失败: {str(e)}")
            
        time.sleep(2)
    
    return results


# 执行流程
if __name__ == "__main__":
        QUESTIONS, IMAGE_URLS = read_table('D:/作业/程序设计/小组作业/智能体测试代码/wenxin/0_output.xlsx',start_row=1, end_row=42)#  改行数
        answers = batch_query(QUESTIONS, IMAGE_URLS, sessionId)
        with open("output2.txt", "w", encoding="utf-8") as f:  # 新增：打开文件准备写入
            for i, ans in enumerate(answers):
                output = f"\n问题 {i+1} 的完整响应:\n"
                output += f"状态码: {ans.get('status_code')}\n"
                output += f"原始响应: {ans.get('raw_response')}\n"  # 直接输出原始文本
                if "parsed_response" in ans:
                    output += f"解析后的JSON: {ans.get('parsed_response')}\n"
                if "error" in ans:
                    output += f"错误信息: {ans.get('error')}\n"
                print(output)  # 保留控制台输出
                f.write(output)  # 写入文件
    