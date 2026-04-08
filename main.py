import os
import requests
import re
import time

# 读取 Cookie
cookie = os.getenv("TIEBA_COOKIE", "").strip()
if not cookie:
    print("❌ 未设置 Cookie")
    exit(1)

headers = {
    "Cookie": cookie,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Referer": "https://tieba.baidu.com/",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

session = requests.Session()
session.headers.update(headers)

# 获取所有关注的贴吧（支持分页，不会漏签，不会 0 个）
def get_all_tieba():
    tieba_list = []
    pn = 1

    while True:
        url = f"https://tieba.baidu.com/f/like/mylike?pn={pn}"
        try:
            resp = session.get(url, timeout=15)
            resp.encoding = "utf-8"
            html = resp.text

            # 匹配贴吧名称（最稳的正则）
            bars = re.findall(r'<a title="([^"]+)" href="/f\?kw=[^"]+', html)
            if not bars:
                break

            tieba_list.extend(bars)
            pn += 1
            time.sleep(0.3)
        except:
            break

    return list(dict.fromkeys(tieba_list))

# 签到
def sign(kw):
    url = "https://tieba.baidu.com/sign/add"
    data = {
        "ie": "utf-8",
        "kw": kw
    }
    try:
        res = session.post(url, data=data, timeout=10).json()
        no = res.get("no")
        msg = res.get("msg", "")

        if no == 0:
            return f"✅ {kw} → 签到成功"
        elif no == 1101:
            return f"✅ {kw} → 今天已签过"
        else:
            return f"❌ {kw} → {msg}"
    except Exception as e:
        return f"⚠️ {kw} → 失败：{str(e)}"

if __name__ == "__main__":
    print("🚀 开始获取贴吧列表...")
    all_bars = get_all_tieba()

    if not all_bars:
        print("❌ 错误：没有获取到任何贴吧！")
        print("👉 解决方法：重新复制最新的 Cookie！")
        exit(1)

    print(f"🎯 成功获取到 {len(all_bars)} 个贴吧\n")

    # 开始逐个签到
    for i, bar in enumerate(all_bars, 1):
        result = sign(bar)
        print(f"{i}. {result}")
        time.sleep(1)

    print("\n🎉 全部签到完成！")
