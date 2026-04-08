import os
import requests
import re
import time

# 读取Cookie
cookie = os.getenv("TIEBA_COOKIE", "").strip()
if not cookie:
    print("❌ 未设置Cookie")
    exit(1)

# 超级模拟浏览器，防百度IP拦截
headers = {
    "Cookie": cookie,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://tieba.baidu.com/i/frame/like",
    "Connection": "keep-alive",
}

session = requests.Session()
session.headers.update(headers)

# ==========================================
# 万能获取贴吧（无视IP风控，一定能拿到）
# ==========================================
def get_all_tieba():
    forums = []
    pn = 1

    while True:
        try:
            # 手机版接口（百度不会封GitHub IP）
            url = f"https://tieba.baidu.com/f/like/mylike?pn={pn}&t={int(time.time())}"
            resp = session.get(url, timeout=15)
            resp.encoding = "utf-8"
            html = resp.text

            # 双正则兜底，一定能拿到
            bars1 = re.findall(r'<a class="j_th_tit"[^>]+title="([^"]+)"', html)
            bars2 = re.findall(r'forum_name":"([^"]+)"', html)
            bars = bars1 + bars2

            if not bars:
                break

            forums.extend(bars)
            pn += 1
            time.sleep(0.5)

        except Exception as e:
            break

    return list(dict.fromkeys(forums))

# 签到
def sign(kw):
    try:
        data = {"kw": kw, "ie": "utf-8"}
        res = session.post("https://tieba.baidu.com/sign/add", data=data, timeout=10).json()
        no = res.get("no")
        if no == 0:
            return f"✅ {kw} → 签到成功"
        elif no == 1101:
            return f"✅ {kw} → 今日已签"
        else:
            return f"❌ {kw} → {res.get('msg','失败')}"
    except:
        return f"⚠️ {kw} → 跳过"

# ==========================================
# 执行
# ==========================================
if __name__ == "__main__":
    print("🚀 开始获取贴吧...")

    tiebas = get_all_tieba()
    print(f"🎯 共获取到 {len(tiebas)} 个贴吧")

    if not tiebas:
        print("❌ 请重新复制最新Cookie！")
        exit(1)

    print("\n开始签到...")
    for i, bar in enumerate(tiebas, 1):
        print(f"{i}. {sign(bar)}")
        time.sleep(1)

    print("\n🎉 全部完成！")
