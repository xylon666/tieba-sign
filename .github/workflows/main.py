import os
import requests

cookie = os.environ.get("TIEBA_COOKIE", "")
if not cookie:
    print("未设置 Cookie")
    exit()

headers = {
    "Cookie": cookie,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
}

# 获取关注的贴吧
def get_like_tieba():
    url = "https://tieba.baidu.com/f/like/mylike"
    r = requests.get(url, headers=headers)
    import re
    tbs = re.findall(r'\/f\?kw=([^&"]+)', r.text)
    return list(set(tbs))

# 签到
def sign(kw):
    url = "https://tieba.baidu.com/sign/add"
    data = {
        "ie": "utf-8",
        "kw": kw
    }
    try:
        res = requests.post(url, data=data, headers=headers).json()
        print(f"{kw}：{res.get('msg', '签到成功')}")
    except Exception as e:
        print(f"{kw} 失败：{e}")

if __name__ == "__main__":
    tiebas = get_like_tieba()
    print(f"共 {len(tiebas)} 个贴吧")
    for kw in tiebas:
        sign(kw)
