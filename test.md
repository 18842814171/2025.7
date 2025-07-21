获取 AccessToken

access_token 的存储与更新：

    access_token 的存储至少要保留 1024 个字符空间。
    access_token 的有效期目前为 1 个月，中控服务器需要根据这个有效时间提前去刷新。
    建议开发者使用中控服务器统一获取和刷新 access_token，由中控服务器统一管理分发 access_token 到其他业务产品线。
    GET https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=CLIENT_ID&client_secret=CLIENT_SECRET
请求参数
参数	类型	是否必填	说明
grant_type	String	是	固定为：client_credentials
client_id	String	是	• 对于智能体部署
智能体 ID，可在「文心智能体平台-管理中心-智能体-部署-api 调用」获得。（要先在平台创建智能体并发布上线）
• 对于插件
插件的 ID，可在「文心智能体平台 - 插件 - XX插件」页中获得。（要先在平台创建插件）
client_secret	String	是	• 对于智能体部署
智能体的 Secret Key，可在「文心智能体平台-管理中心-智能体-部署- api 调用」获得，请妥善保存。
• 对于插件
插件的 Secret Key，可在「文心智能体平台- 插件 - XX插件」页中获得，请妥善保存
  GET "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=OLdnBMrbRvMPaYibFiXyPlfPGKWjgabD&client_secret=cebrF4cfSm89XrfiVcuSE6hv82fs0OKe"




## 每次在 VS Code 中新建一个 PowerShell 终端时，终端会启动一个新的会话，之前的变量（如 $appId 和 $secretKey）不会自动保留。
$appId="OLdnBMrbRvMPaYibFiXyPlfPGKWjgabD"
$secretKey="UPoJWIkWgoe79Sy4H5aJpPxhkrlDY2SH"

# 构造请求 URL
$tokenUrl = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=$clientId&client_secret=$clientSecret"

# 发送 GET 请求
$response = Invoke-RestMethod -Uri $tokenUrl -Method Get

# 输出 access_token
Write-Output "Access Token: $($response.access_token)"
Write-Output "Expires In: $($response.expires_in) 秒"


# 测试基础连通性（返回HTTP 200表示网络通）
curl -I "https://agentapi.baidu.com"

# 测试真实API端点（隐藏敏感信息）
curl -X POST "https://agentapi.baidu.com/assistant/conversation?appId=OLdnBMrbRvMPaYibFiXyPlfPGKWjgabD&secretKey=UPoJWIkWgoe79Sy4H5aJpPxhkrlDY2SH"  -H "Content-Type: application/json"   -d '{"message":{"content":{"type":"text","value":{"showText":"你好"}}}'
# 需要安装curl（Windows 10+自带）
curl.exe -X POST `
  "https://agentapi.baidu.com/assistant/conversation?appId=$appId&secretKey=$secretKey" `
  -H "Content-Type: application/json" `
  -d '{"message":{"content":{"type":"text","value":{"showText":"你好"}}}}'

  curl --location 'https://agentapi.baidu.com/assistant/conversation?appId={appId}&secretKey={secretKey}' --header 'Content-Type: application/json' --data '{
    "message": {
        "content": {
            "type": "text",
            "value": {
                "showText": "你好"
            }
        }
    },
    "source": "web",
    "from": "openapi",
    "openId": "xxx"
}'
Invoke-WebRequest -Uri "https://agentapi.baidu.com/assistant/conversation?appId=$appId&secretKey=$secretKey" `
-Method Post `
-Headers @{"Content-Type"="application/json"} `
-Body '{
    "message": {
        "content": {
            "type": "text",
            "value": {
                "showText": "你好"
            }
        }
    },
    "source": "web",
    "from": "openapi",
    "openId": "test_user_001"
}'

==deepseek给的，能响应，响应内容为空===
Invoke-WebRequest -Uri "https://agentapi.baidu.com/assistant/conversation?appId=$appId&secretKey=$secretKey" `
-Method Post `
-Headers @{"Content-Type"="application/json"} `
-Body '{
    "message": {
        "content": {
            "type": "text",
            "value": {
                "showText": "你好"
            }
        }
    },
    "source": "web",
    "from": "openapi",
    "openId": "test_user_001"
}'


==grok给的==
$appId = "your_actual_app_id"
$secretKey = "your_actual_secret_key"
$uri = "https://agentapi.baidu.com/assistant/conversation?appId=$appId&secretKey=$secretKey"
$body = @{
    message = @{
        content = @{
            type = "text"
            value = @{ showText = "你好" }
        }
    }
    source = "web"
    from = "openapi"
    openId = "test_user_001"
} | ConvertTo-Json -Depth 10

try {
    $response = Invoke-RestMethod -Uri $uri -Method Post -Headers @{"Content-Type"="application/json"} -Body $body
    Write-Output $response
} catch {
    Write-Error "请求失败: $_"
}

json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
这个错误 JSONDecodeError: Expecting value 表明服务器返回的响应不是有效的 JSON 格式（可能是空响应、HTML 错误页面或非 JSON 数据）。



    Cookie 字符串包含非法字符：如换行符、未转义的双引号（"）或特殊符号（@、=、°C 等）。

    Python 请求的 Cookie 格式要求：必须是 键值对字典，或直接传递原始字符串（需严格格式化）。
在 Python 中，如果 Cookie 字符串包含特殊字符（如 ", ', \, \n, 不可见控制字符等），可能会导致 HTTP 请求失败或解析错误。以下是 清除 Cookie 特殊字符 的方法：
方法 1：使用 re 正则表达式过滤
python

import re

def clean_cookie(cookie):
    # 只保留字母、数字、常见符号（=, ;, _, -, .）
    return re.sub(r'[^\w=;_,.-]', '', cookie)

# 示例
dirty_cookie = 'BIDUPSID="E42263344D69156A8B4332C5D82C4EC2"; PSTM=1750499427; \nMAWEBCUID=web_yPxuEzOSMNKiOkRWzUOPBmdoqiCrZuJPhpSMXvHDVEKMetSnvd;'
clean = clean_cookie(dirty_cookie)
print(clean)

输出：
text

BIDUPSID=E42263344D69156A8B4332C5D82C4EC2;PSTM=1750499427;MAWEBCUID=web_yPxuEzOSMNKiOkRWzUOPBmdoqiCrZuJPhpSMXvHDVEKMetSnvd;

方法 2：使用 str.strip() 和 str.replace()

如果问题主要是换行符、引号等：
python

def clean_cookie(cookie):
    return cookie.strip().replace('"', '').replace("'", "").replace("\n", "")

# 示例
dirty_cookie = '\nBIDUPSID="E42263344D69156A8B4332C5D82C4EC2";\n'
clean = clean_cookie(dirty_cookie)
print(clean)

输出：
text

BIDUPSID=E42263344D69156A8B4332C5D82C4EC2;

方法 3：逐字符检查（严格模式）

如果 Cookie 必须严格符合规范（如仅允许 RFC 6265 允许的字符）：
python

def clean_cookie(cookie):
    allowed_chars = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        "=;,_-."
    )
    return ''.join(c for c in cookie if c in allowed_chars)

方法 4：使用 http.cookiejar 解析（推荐）

如果 Cookie 是标准格式（name=value; name2=value2），可以用 Python 内置库解析后重建：
python

from http.cookiejar import CookieJar
from urllib.request import Request, build_opener

def clean_cookie(cookie):
    jar = CookieJar()
    req = Request("http://example.com", headers={"Cookie": cookie})
    jar.extract_cookies(req, req)
    return "; ".join(f"{c.name}={c.value}" for c in jar)

# 示例
dirty_cookie = 'BIDUPSID="E42263344D69156A8B4332C5D82C4EC2"; invalid_char=你好;'
clean = clean_cookie(dirty_cookie)
print(clean)  # 自动过滤非 ASCII 字符

输出：
text

BIDUPSID=E42263344D69156A8B4332C5D82C4EC2

注意事项

    保留关键符号：确保 =, ; 等分隔符不被删除。

    编码问题：如果 Cookie 含非 ASCII 字符（如中文），可能需要先编码：
    python

cookie = cookie.encode('ascii', 'ignore').decode('ascii')

测试验证：清理后手动检查 Cookie 是否仍能用于请求。优先使用方法 1（正则）或方法 4（http.cookiejar），它们能处理大多数情况。

# ！！！# 每次前端获取sessionid方法：F12--网络-过滤conversation--找post

(.venv) PS D:\作业\其他\测试代码> & D:/作业/其他/测试代码/.venv/Scripts/python.exe d:/作业/其他/测试代码/zaiyong.py

问题 1 的完整响应:
状态码: 200
原始响应: event:message
data:{"status":0,"message":"succ","sessionId":"1752583460513264640","logid":"3307064958","data":{"message":{"content":null,"endTurn":false,"isRegenerated":false,"msgId":"86fba6ebfc114d04b45bdf5db6af227e","msgType":"normal","pageToken":"","updateTime":"","runLog":null},"qid":"3307064958"}}

event:message
data:{"status":0,"message":"succ","sessionId":"1752583460513264640","logid":"3307064958","data":{"message":{"content":null,"endTurn":false,"isRegenerated":false,"msgId":"86fba6ebfc114d04b45bdf5db6af227e","msgType":"normal","pageToken":"","updateTime":"1752585697000","runLog":null},"qid":"3307064958"}}

event:ping

event:message
data:{"status":0,"message":"succ","sessionId":"1752583460513264640","logid":"3307064958","data":{"message":{"content":null,"endTurn":false,"isRegenerated":false,"msgId":"86fba6ebfc114d04b45bdf5db6af227e","msgType":"normal","pageToken":"","updateTime":"1752585697000","runLog":null},"qid":"3307064958"}}

event:message
data:{"status":0,"message":"succ","sessionId":"1752583460513264640","logid":"3307064958","data":{"message":{"content":null,"endTurn":false,"isRegenerated":false,"msgId":"86fba6ebfc114d04b45bdf5db6af227e","msgType":"normal","pageToken":"","updateTime":"1752585697000","runLog":{"agentMode":"assistant","from":"platform","isToolSelected":true,"scene":"","source":"","tags":[{"tagCateCode":"role_agent_label","tagCateName":"C端标签-角色维度","tagValue":"15","tagExt":{}},{"tagCateCode":"industry_domain_agent_label","tagCateName":"C端标签-行业维度- 领域","tagValue":"21","tagExt":{}},{"tagCateCode":"industry_creation_label","tagCateName":"C端标签-行业维度-创作","tagValue":"12","tagExt":{}},{"tagCateCode":"skill_agent_label","tagCateName":"C端标签-技能维度","tagValue":"11","tagExt":{}}]}},"qid":"3307064958"}}

event:message
data:{"status":0,"message":"succ","sessionId":"1752583460513264640","logid":"3307064958","data":{"message":{"content":null,"endTurn":false,"isRegenerated":false,"msgId":"86fba6ebfc114d04b45bdf5db6af227e","msgType":"normal","pageToken":"","updateTime":"1752585697000","runLog":{"modelName":"c83c819146fab13446aa9c0761f9747f"}},"qid":"3307064958"}}

event:message
data:{"status":0,"message":"succ","sessionId":"1752583460513264640","logid":"3307064958","data":{"message":{"content":[{"sectionId":"","readOnly":false,"isFinished":false,"progress":{"stepId":"1","status":0,"name":"memory","content":"正在查找信息","toolsStatus":[{"isBuiltinTool":true,"status":"start","toolName":"","actionName":"正在查找信息","actionContent":""}],"time":1752585697568,"ext":""}}],"endTurn":false,"isRegenerated":false,"msgId":"86fba6ebfc114d04b45bdf5db6af227e","msgType":"normal","pageToken":"","updateTime":"1752585697000","runLog":null},"qid":"3307064958"}}

event:message
data:{"status":0,"message":"succ","sessionId":"1752583460513264640","logid":"3307064958","data":{"message":{"content":[{"sectionId":"","readOnly":false,"isFinished":false,"progress":{"stepId":"1","status":1,"name":"memory","content":"长期记忆检索完成","toolsStatus":[{"isBuiltinTool":true,"status":"finish","toolName":"","actionName":"长期记忆检索完成","actionContent":""}],"time":1752585697599,"ext":""}}],"endTurn":false,"isRegenerated":false,"msgId":"86fba6ebfc114d04b45bdf5db6af227e","msgType":"normal","pageToken":"","updateTime":"1752585697000","runLog":null},"qid":"3307064958"}}

event:message
data:{"status":0,"message":"succ","sessionId":"1752583460513264640","logid":"3307064958","data":{"message":{"content":[{"sectionId":"","readOnly":false,"isFinished":false,"progress":{"stepId":"2","status":0,"name":"official_tool","content":"正在使用图片理解","function":{"name":"图片理解","actionInfo":[{"name":"正在使用","content":"","error":""}]},"toolsStatus":[{"isBuiltinTool":true,"status":"start","toolName":"图片理解","actionName":"正在使用","actionContent":""}],"time":1752585699707,"ext":""}}],"endTurn":false,"isRegenerated":false,"msgId":"86fba6ebfc114d04b45bdf5db6af227e","msgType":"normal","pageToken":"","updateTime":"1752585699000","runLog":null},"qid":"3307064958"}}

event:ping

event:ping

event:message
data:{"status":0,"message":"succ","sessionId":"1752583460513264640","logid":"3307064958","data":{"message":{"content":[{"sectionId":"","readOnly":false,"isFinished":false,"progress":{"stepId":"2","status":1,"name":"official_tool","content":"使用完成 图片理解","function":{"name":"图片理解","actionInfo":[{"name":"使用完成","content":"","error":""}]},"toolsStatus":[{"isBuiltinTool":true,"status":"finish","toolName":"图片理解","actionName":"使用完成","actionContent":""}],"time":1752585708038,"ext":""}}],"endTurn":false,"isRegenerated":false,"msgId":"86fba6ebfc114d04b45bdf5db6af227e","msgType":"normal","pageToken":"","updateTime":"1752585708000","runLog":null},"qid":"3307064958"}}

event:message
data:{"status":0,"message":"succ","sessionId":"1752583460513264640","logid":"3307064958","data":{"message":{"content":[{"sectionId":"","readOnly":false,"isFinished":false,"progress":{"stepId":"3","status":0,"name":"official_tool","content":"正在使用图片理解","function":{"name":"图片理解","actionInfo":[{"name":"正在使用","content":"","error":""}]},"toolsStatus":[{"isBuiltinTool":true,"status":"start","toolName":"图片理解","actionName":"正在使用","actionContent":""}],"time":1752585708872,"ext":""}}],"endTurn":false,"isRegenerated":false,"msgId":"86fba6ebfc114d04b45bdf5db6af227e","msgType":"normal","pageToken":"","updateTime":"1752585708000","runLog":null},"qid":"3307064958"}}

event:ping

event:ping

event:message
data:{"status":0,"message":"succ","sessionId":"1752583460513264640","logid":"3307064958","data":{"message":{"content":[{"sectionId":"","readOnly":false,"isFinished":false,"progress":{"stepId":"3","status":1,"name":"official_tool","content":"使用完成 图片理解","function":{"name":"图片理解","actionInfo":[{"name":"使用完成","content":"","error":""}]},"toolsStatus":[{"isBuiltinTool":true,"status":"finish","toolName":"图片理解","actionName":"使用完成","actionContent":""}],"time":1752585714255,"ext":""}}],"endTurn":false,"isRegenerated":false,"msgId":"86fba6ebfc114d04b45bdf5db6af227e","msgType":"normal","pageToken":"","updateTime":"1752585714000","runLog":null},"qid":"3307064958"}}

event:message
data:{"status":0,"message":"succ","sessionId":"1752583460513264640","logid":"3307064958","data":{"message":{"content":[{"sectionId":"","readOnly":false,"isFinished":false,"progress":{"stepId":"4","status":0,"name":"generate","content":"信息整理","toolsStatus":[{"isBuiltinTool":true,"status":"start","toolName":"","actionName":"信息整理","actionContent":""}],"time":0,"ext":""}}],"endTurn":false,"isRegenerated":false,"msgId":"86fba6ebfc114d04b45bdf5db6af227e","msgType":"normal","pageToken":"","updateTime":"1752585717000","runLog":null},"qid":"3307064958"}}

event:message
data:{"status":0,"message":"succ","sessionId":"1752583460513264640","logid":"3307064958","data":{"message":{"content":[{"sectionId":"1","readOnly":false,"dataType":"markdown","isFinished":false,"data":{"antiFlag":0,"isIntervene":false,"showType":"append","text":"图片","type":"txt"}}],"endTurn":false,"isRegenerated":false,"msgId":"86fba6ebfc114d04b45bdf5db6af227e","msgType":"normal","pageToken":"","updateTime":"1752585717000","runLog":null},"qid":"3307064958"}}

event:ping

event:message
data:{"status":0,"message":"succ","sessionId":"1752583460513264640","logid":"3307064958","data":{"message":{"content":[{"sectionId":"1","readOnly":false,"dataType":"markdown","isFinished":false,"data":{"antiFlag":0,"isIntervene":false,"showType":"append","text":"中是婴儿电动磨甲器，适合宝宝满月后使用。","type":"txt"}}],"endTurn":false,"isRegenerated":false,"msgId":"86fba6ebfc114d04b45bdf5db6af227e","msgType":"normal","pageToken":"","updateTime":"1752585717000","runLog":null},"qid":"3307064958"}}

event:message
data:{"status":0,"message":"succ","sessionId":"1752583460513264640","logid":"3307064958","data":{"message":{"content":[{"sectionId":"1","readOnly":false,"dataType":"markdown","isFinished":false,"data":{"antiFlag":0,"isIntervene":false,"showType":"append","text":"具体磨头选择需视年龄和指甲状况。产品通常","type":"txt"}}],"endTurn":false,"isRegenerated":false,"msgId":"86fba6ebfc114d04b45bdf5db6af227e","msgType":"normal","pageToken":"","updateTime":"1752585718000","runLog":null},"qid":"3307064958"}}

event:message
data:{"status":0,"message":"succ","sessionId":"1752583460513264640","logid":"3307064958","data":{"message":{"content":[{"sectionId":"1","readOnly":false,"dataType":"markdown","isFinished":false,"data":{"antiFlag":0,"isIntervene":false,"showType":"append","text":"色彩鲜艳、设计安全，适合婴儿。至于成人使用","type":"txt"}}],"endTurn":false,"isRegenerated":false,"msgId":"86fba6ebfc114d04b45bdf5db6af227e","msgType":"normal","pageToken":"","updateTime":"1752585719000","runLog":null},"qid":"3307064958"}}

event:message
data:{"status":0,"message":"succ","sessionId":"1752583460513264640","logid":"3307064958","data":{"message":{"content":[{"sectionId":"1","readOnly":false,"dataType":"markdown","isFinished":false,"data":{"antiFlag":0,"isIntervene":false,"showType":"append","text":"，一般不建议，因成人指甲硬度和宝宝不同。","type":"txt"}}],"endTurn":false,"isRegenerated":false,"msgId":"86fba6ebfc114d04b45bdf5db6af227e","msgType":"normal","pageToken":"","updateTime":"1752585719000","runLog":null},"qid":"3307064958"}}

event:message
data:{"status":0,"message":"succ","sessionId":"1752583460513264640","logid":"3307064958","data":{"message":{"content":[{"sectionId":"1","readOnly":false,"dataType":"markdown","isFinished":true,"data":{"antiFlag":0,"isIntervene":false,"showType":"append","text":"需更多信息请查阅说明书。","type":"txt"}}],"endTurn":false,"isRegenerated":false,"msgId":"86fba6ebfc114d04b45bdf5db6af227e","msgType":"normal","pageToken":"","updateTime":"1752585720000","runLog":null},"qid":"3307064958"}}

event:ping

event:message
data:{"status":0,"message":"succ","sessionId":"1752583460513264640","logid":"3307064958","data":{"message":{"content":null,"endTurn":false,"isRegenerated":false,"msgId":"86fba6ebfc114d04b45bdf5db6af227e","msgType":"normal","pageToken":"","suggestion":{"title":"","type":"suggestion","suggestionList":[{"text":"这个磨甲器适合多大的宝宝用？"},{"text":"磨甲器有哪些不同的磨头可以选择？"},{"text":"使用磨甲器有什么需要注意的？"}]},"updateTime":"1752585721000","runLog":null},"qid":"3307064958"}}

event:message
data:{"status":0,"message":"succ","sessionId":"1752583460513264640","logid":"3307064958","data":{"message":{"content":[{"sectionId":"","readOnly":false,"isFinished":false,"progress":{"stepId":"4","status":1,"name":"generate","content":"信息整理","toolsStatus":[{"isBuiltinTool":true,"status":"finish","toolName":"","actionName":"信息整理","actionContent":""}],"time":0,"ext":""}}],"endTurn":false,"isRegenerated":false,"msgId":"86fba6ebfc114d04b45bdf5db6af227e","msgType":"normal","pageToken":"","updateTime":"1752585721000","runLog":null},"qid":"3307064958"}}

event:message
data:{"status":0,"message":"succ","sessionId":"1752583460513264640","logid":"3307064958","data":{"message":{"content":[{"sectionId":"","readOnly":false,"isFinished":false,"feedback":{"feDislikeKey":"ps_2828283161_1455042710","feLikeKey":"ps_2828283161_1455042710"}}],"endTurn":true,"isRegenerated":false,"msgId":"86fba6ebfc114d04b45bdf5db6af227e","msgType":"normal","pageToken":"86fba6ebfc114d04b45bdf5db6af227e","updateTime":"1752585721000","runLog":null},"qid":"3307064958"}}

event:message
data:{"status":0,"message":"succ","sessionId":"1752583460513264640","logid":"3307064958","data":{"message":{"content":null,"endTurn":false,"isRegenerated":false,"msgId":"86fba6ebfc114d04b45bdf5db6af227e","msgType":"normal","pageToken":"","updateTime":"1752585721000","runLog":null},"qid":"3307064958"}}

event:message
data:{"status":0,"message":"succ","sessionId":"1752583460513264640","logid":"3307064958","data":{"message":{"content":null,"endTurn":false,"isRegenerated":false,"msgId":"86fba6ebfc114d04b45bdf5db6af227e","msgType":"normal","pageToken":"","updateTime":"","runLog":null},"qid":"3307064958"}}


(.venv) PS D:\作业\其他\测试代码> 每次先前端获取sessionid,改sessionid再进行批量实验


# 智谱清言

https://github.com/MetaGLM/glm-cookbook/blob/main/glms/api/glms_api.ipynb 


# Minimax
https://www.minimax.io/platform/document/quickstart?key=6842ad59eb26e680a34df0d7
https://www.minimax.io/platform/document/platform%20introduction?key=66701c8e1d57f38758d58198   api documentation
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJsaW5kYSIsIlVzZXJOYW1lIjoibGluZGEiLCJBY2NvdW50IjoiIiwiU3ViamVjdElEIjoiMTk0NTQwMzIwOTQxMzU2MjUzMiIsIlBob25lIjoiIiwiR3JvdXBJRCI6IjE5NDU0MDMyMDk0MDkzNjgyMjgiLCJQYWdlTmFtZSI6IiIsIk1haWwiOiJmendreGVxbTEwQGdtYWlsLmNvbSIsIkNyZWF0ZVRpbWUiOiIyMDI1LTA3LTE2IDE3OjA2OjA0IiwiVG9rZW5UeXBlIjoxLCJpc3MiOiJtaW5pbWF4In0.FfhhS8fvpVBsDPgJNeUmyiQPV0I3-vWY2v6qb9fQN_Kv9spCYDd3dg8QW6e_UCZt24aGDofPHrmoxuV577VkGLWlhGl7rAxLcOAkNv567v2bPjNoyCWyfr6r2BIy-UVtlEzhM4Hxux3TfvvX3yootr3jaAnAexdAtX4EnqYZUtDzKda8iVNVJFp35zKf0OZMELEcsTYXPm6uEiGZNR113XpnFnpBJLhT_QRCSs9KADIxoX96Ul-LsRybWkgl1q1Vom0UnDdPixScRDBGZTxJQXFPy8Cr6gtWIQFmL0LFBUUGaoosaXqGKJWMN_b88M8l0rIfXuszJ1EzViy7ioqhuA

api key

既然 前端可以处理图片，但 API 返回“图片理解功能暂未开放”，说明百度智能体的图片分析功能 仅对前端开放，未开放给公开API。以下是具体分析和解决方案：
1. 根本原因

    前端特权：百度智能体的前端（Web/小程序）可能使用 内部接口 或 特殊权限 调用图片分析，而公开API受限。

    安全策略：图片分析可能涉及计算成本或合规审核，百度仅允许前端可控的场景使用。

2. 如何让API也能处理图片？
(1) 方案一：模拟前端请求（需抓包）

如果前端能成功调用，可以 抓取完整请求 并复现：

    在浏览器中抓包：

        打开 Chrome DevTools → Network → 筛选 XHR 或 Fetch。

        上传图片并提问，找到包含图片数据的请求（通常是 POST 请求）。

        记录：

            URL（可能是内部接口，如 https://agent-proxy.baidu.com/internal/chat）

            Headers（尤其是 Cookie、Authorization）

            Request Body（检查图片是 URL 还是 base64）。

    用Python模拟请求：
    python

import requests

# 从前端复制的URL和Headers
url = "https://agent-proxy.baidu.com/internal/chat"  # 示例
headers = {
    "Content-Type": "application/json",
    "Cookie": "BAIDUID=xxx; BDUSS=xxx",  # 从浏览器复制
    "Referer": "https://smartapps.baidu.com/",
}

# 从前端复制的Request Body
data = {
    "appId": "OLdnBMrbRvMPaYibFiXyPlfPGKWjgabD",
    "content": {
        "query": {
            "type": "multimodal",
            "value": [
                {"type": "text", "value": {"text": "这是什么图片？"}},
                {"type": "image", "value": {"imageUrl": "https://xxx.com/image.jpg"}}
            ]
        }
    }
}

response = requests.post(url, json=data, headers=headers)
print(response.json())

===json: unknown field \"skip_info\""

博查 api 密钥  sk-003863984927481683f8e04acd26a02b

博查AI Web Search API：

    根据博查AI开放平台文档（https://open.bochaai.com），Web Search API端点为https://api.bochaai.com/v1/web-search，支持实时搜索网页、新闻、图片等内容。
    请求需要API密钥（通过WeChat登录后在“API KEY Management”生成），支持参数如query（搜索关键词）、freshness（时间范围）、summary（是否返回摘要）、count（结果数量）。
    示例请求：
    bash

        curl --location 'https://api.bochaai.com/v1/web-search' \
        --header 'Authorization: Bearer Your-API-KEY' \
        --header 'Content-Type: application/json' \
        --data '{ "query": "Shanghai weather", "freshness": "oneWeek", "summary": true, "count": 5 }'
        响应为JSON格式，包含标题、链接、摘要等。
    MiniMax的多模态支持：
        MiniMax-M1支持图像输入（Base64编码或URL），无需工具调用即可处理图像内容。
        联网搜索需要Function Calling，通过web_search工具触发博查AI的搜索API。
    任务需求：
        上传本地图像（例如，上海的照片）。
        提出问题（如“Search for the recent weather in Shanghai”）。
        MiniMax模型分析图像并生成搜索查询，调用博查AI Web Search API获取结果，最终返回简短回答。
    挑战：
        需将图像描述与搜索查询结合，可能需要两次API调用：第一次让MiniMax分析图像并生成搜索查询，第二次将搜索结果反馈给MiniMax生成最终回答。
        博查AI API密钥需单独获取，当前代码使用MiniMax API密钥。

获取博查AI API密钥

    访问https://open.bochaai.com，点击右上角“Login”按钮，使用WeChat扫码登录（目前仅支持WeChat登录，）。

登录后，点击“API KEY Management”，点击“Create API KEY”生成密钥。
复制密钥并保存，格式为sk-****（需替换到代码中）。
代码说明

    博查AI API配置：
        添加BOCHA_URL和BOCHA_API_KEY常量，需替换为实际博查AI密钥（通过https://open.bochaai.com获取）。
        call_bocha_search函数调用博查AI的Web Search API，设置freshness为oneWeek以获取近期结果，summary=True返回摘要，count=5限制结果数量。
    图像处理：
        使用encode_image函数将本地图像转换为Base64编码，嵌入到messages的image_url字段。
        用户消息包含图像和文本提示：“Search for the recent weather in Shanghai based on this image”。
    两阶段请求：
        第一次请求：MiniMax分析图像并生成搜索查询（如“Shanghai weather”），通过tool_calls返回web_search指令。
        第二次请求：将博查AI搜索结果（search_result）作为tool消息反馈给MiniMax，生成最终简短回答（100字以内）。
    流式输出：
        保留stream=True，通过iter_lines()处理流式响应，拼接content字段获取查询和最终回答。
    参数保留：
        保持原代码的model（MiniMax-M1）、temperature（0.5）、top_p（0.95），max_tokens分别为50（生成查询）和100（最终回答）。

运行说明

    替换图像路径：
        修改image_path为实际图像路径（如"./shanghai.jpg"），支持JPEG/PNG格式。
    替换博查AI API密钥：
        将BOCHA_API_KEY替换为从https://open.bochaai.com获取的密钥。
    测试：
        运行代码，上传上海相关图像（如城市景观），模型会生成类似“Shanghai weather”查询，调用博查AI API获取结果，最终输出如：“Shanghai: Sunny, 3~9°C, Northeast wind <3”。
    错误处理：
        如果博查AI API返回错误（如401），检查密钥有效性。
        如果MiniMax输出截断，尝试增加max_tokens（如2048）或检查网络稳定性。


需要修改的部分

    时间戳 (time_ms)
        原因: publicEncrypt 使用 md5(time.toString())，每次请求的时间戳不同会影响 yy 值的计算。
        修改方式:
            保持动态时间：继续使用 time_ms = int(time.time() * 1000)，确保每次请求使用当前时间（例如 2025-07-17 20:31 HKT）。
            固定时间：如果服务器要求特定时间戳（如 1752741005000），在每次请求前手动设置：
            python

time_ms = 1752741005000  # 替换为服务器要求的固定值
循环时动态更新：如果多次请求，在循环中更新：
python

        for i in range(num_requests):
            time_ms = int(time.time() * 1000) + i  # 避免时间戳重复
            yy = compute_yy(characterID, chatID, file_path, time_ms, pathname, body)

文件路径 (file_path)

    原因: 每次输入可能涉及不同文件，md5(file[0:1024]) 会因文件内容变化。
    修改方式:
        动态指定文件：根据请求次数传入不同文件路径：
        python

        file_paths = ["path/to/file1.jpg", "path/to/file2.jpg"]  # 不同文件列表
        for file_path in file_paths:
            yy = compute_yy(characterID, chatID, file_path, time_ms, pathname, body)
        验证文件存在：确保每次文件路径有效。

请求体数据 (body)

    原因: publicEncrypt 使用 body（POST 请求时），不同输入可能有不同 msgContent 或其他字段。
    修改方式:
        动态更新 body：根据次数修改 msgContent 或其他字段：
        python

        bodies = [
            {"msgContent": "message 1", "chatID": chatID, ...},
            {"msgContent": "message 2", "chatID": chatID, ...}
        ]
        for body in bodies:
            yy = compute_yy(characterID, chatID, file_path, time_ms, pathname, body)
        保持一致：如果 body 不变，可复用同一 body。

查询参数 (params)

    原因: pathname 包含 params，不同请求可能需要不同的 uuid 或 unix。
    修改方式:
        动态生成 params：每次请求生成新 uuid 或 unix：
        python

import uuid
for _ in range(num_requests):
    params["uuid"] = str(uuid.uuid4())
    params["unix"] = str(int(time.time() * 1000))
    pathname = "/v4/api/chat/msg?" + "&".join(f"{k}={v}" for k, v in params.items())
    yy = compute_yy(characterID, chatID, file_path, time_ms, pathname, body)