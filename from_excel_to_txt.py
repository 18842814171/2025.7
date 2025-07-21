import requests
import uuid
import time

# 配置参数
API_URL = "https://agent-proxy-ws.baidu.com/agent/call/conversation"
HEADERS = {
    "Content-Type": "application/json",
    "Cookie": "BIDUPSID=E42263344D69156A8B4332C5D82C4EC2;PSTM=1750499427;H_PS_PSSID=60276_62325_63147_63326_63275_63725_63881_63911_63903_63950_63947_63995_64008_64016_64027_64058_64055_64050;BAIDUID=E42263344D69156A8B4332C5D82C4EC2FG=1;H_WISE_SIDS=60276_62325_63147_63326_63275_63725_63708_63754_63800_63881_63911_63903_63950_63947_63995_64008_64016_64027_64036;MAWEBCUID=web_yPxuEzOSMNKiOkRWzUOPBmdoqiCrZuJPhpSMXvHDVEKMetSnvd;BDUSS=ItVkRsSjRwSkozaW91ZzIwckRYdDJxNXRLY0VMWGVxQm15Y0N2cH5wa0F-SmRvRVFBQUFBJCQAAAAAAQAAAAEA9-9a57-4a14-85fa-2951c8fc335bss=md4i6f2osl=btt=eujbcn=https3A2F2Ffclog.baidu.com2Flog2Fweirwood3Ftype3Dperfld=4wsc;__bid_n=197e901046a6864c426a5f;ZFY=Md9V7eay3ulO2ySktPjZF26vCTy82mA2UVdvunlMvT0C;delPer=0;PSINO=1;BA_HECTOR=0l0k04a5al8121a405ah84ag20a4031k7c6at25;ab_sr=1.0.1_ZDlmZWQwNzEwYzM0YzcxZTQwMGIxNTFiZDI3ZGUzZDg1M2IxMzBmNjQ0NmIwMjI5OTk0MDFmNGU3ZWM0M2Y5YzFkNTMwMDFjYzZkNTRiYzQ3YmYxNGM4YWEyYjM5MWE0YjVkMDI2YmYwOTkyMmZmN2JhODQ3MTY3MjcxYjQxNDU2ZWYxNGI0NTcwN2IyNGQyOTk3ZWRlODlmNzU4NjRiMg==",
    "Referer": "https://smartapps.baidu.com/",
    "Origin": "https://smartapps.baidu.com",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0"
}
APP_ID = "OLdnBMrbRvMPaYibFiXyPlfPGKWjgabD"
sessionId= "1752630883098920226"
# 问题与图片列表（示例）
QUESTIONS = [
   "what color is the plunger? ||| what is a plunger used for? ||| what is the difference between a plunger with a wood handle and one with a plastic handle? ||| what other types of tools are used to remove blockages from pipes and drains?",
   
]
IMAGE_URLS = [
   "http://m.qpic.cn/psc?/V52hKjoK38Z0CJ1GfE4i2T0LHX3e7YvZ/TmEUgtj9EK6.7V8ajmQrEJ0VyazGGxbbn0BtTU0SC9vMjlmPTn98YopqUF2cEXbw7HuQ9abL59j0OtSV98stXmTRMAphnAmGI2FVH029DLI!/mnull&bo=QAZVCEAGVQgBByA!&rf=photolist&t=5",

]


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
    