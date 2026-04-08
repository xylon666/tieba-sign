import os
import requests
import time

# 读取Cookie
cookie = os.getenv("TIEBA_COOKIE", "").strip()
if not cookie:
    print("❌ 未设置 TIEBA_COOKIE 密钥")
    exit(1)

headers = {
    "Cookie": cookie,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://tieba.baidu.com/"
}

# 获取关注的贴吧
def get_like_tieba():
    url = "https://tieba.baidu.com/f/like/mylike"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        import re
        tbs = re.findall(r'\/f\?kw=([^&"\n]+)', r.text)
        return list(set(tbs))
    except Exception as e:
        print(f"❌ 获取贴吧列表失败：{e}")
        return []

# 签到
def sign(kw):
    url = "https://tieba.baidu.com/sign/add"
    data = {"ie": "utf-8", "kw": kw}
    try:
        res = requests.post(url, data=data, headers=headers, timeout=10).json()
        msg = res.get("msg", "成功")
        print(f"✅ {kw}：{msg}")
    except Exception as e:
        print(f"❌ {kw} 失败：{e}")

if __name__ == "__main__":
    print("🚀 开始签到")
    tiebas = get_like_tieba()
    if not tiebas:
        print("❌ 没有获取到任何贴吧，Cookie 可能失效")
        exit(2)
    print(f"✅ 共 {len(tiebas)} 个贴吧")
    for kw in tiebas:
        sign(kw)
        time.sleep(1)
    print("🎉 签到任务完成")
