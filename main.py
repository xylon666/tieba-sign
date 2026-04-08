import requests
import os
import time

# 从环境变量取 Cookie
cookie = os.getenv("TIEBA_COOKIE")
if not cookie:
    print("❌ 未设置 TIEBA_COOKIE")
    exit(1)

headers = {
    "Cookie": cookie,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://tieba.baidu.com/"
}

session = requests.Session()
session.headers.update(headers)

def get_tbs():
    """获取tbs令牌"""
    try:
        res = session.get("https://tieba.baidu.com/dc/common/tbs")
        return res.json().get("tbs", "")
    except:
        return ""

def get_like_forums():
    """分页获取所有关注贴吧"""
    forums = []
    pn = 1
    while True:
        # 分页接口（pn=页数）
        url = f"https://tieba.baidu.com/f/like/mylike?&pn={pn}"
        res = session.get(url)
        html = res.text
        
        # 提取吧名
        import re
        bars = re.findall(r'"title":"([^"]+)"', html)
        if not bars:
            break  # 没更多页，退出
        
        forums.extend(bars)
        pn += 1
        time.sleep(0.5)  # 防封
    
    # 去重
    return list(dict.fromkeys(forums))

def sign(kw, tbs):
    """单个贴吧签到"""
    url = "https://tieba.baidu.com/sign/add"
    data = {"kw": kw, "tbs": tbs, "ie": "utf-8"}
    try:
        res = session.post(url, data=data)
        j = res.json()
        if j.get("no") in (0, 1101):
            return f"✅ {kw}：{'已签' if j.get('no')==1101 else '签到成功'}"
        else:
            return f"❌ {kw}：{j.get('errmsg', '失败')}"
    except Exception as e:
        return f"⚠️ {kw}：{str(e)}"

if __name__ == "__main__":
    tbs = get_tbs()
    if not tbs:
        print("❌ 获取tbs失败，Cookie可能失效")
        exit(1)
    
    # 关键：获取全部关注贴吧
    forums = get_like_forums()
    print(f"🎯 共关注 {len(forums)} 个贴吧\n")
    
    for idx, kw in enumerate(forums, 1):
        msg = sign(kw, tbs)
        print(f"{idx}. {msg}")
        time.sleep(1)  # 延迟防风控
