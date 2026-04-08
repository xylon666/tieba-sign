import os
import requests
import time

# ===================== 配置 =====================
cookie = os.getenv("TIEBA_COOKIE", "").strip()
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

# ===================== 官方接口获取贴吧（永不0） =====================
def get_like_tieba():
    forums = []
    page = 1
    while True:
        url = f"https://tieba.baidu.com/f/like/json/single?pn={page}"
        try:
            res = session.get(url, timeout=10)
            data = res.json()

            # 没有数据了就退出
            if not data.get("forum_list"):
                break

            # 提取所有贴吧名称
            for item in data["forum_list"]:
                forums.append(item["forum_name"])

            page += 1
            time.sleep(0.3)
        except:
            break
    return list(dict.fromkeys(forums))

# ===================== 签到 =====================
def sign(kw):
    url = "https://tieba.baidu.com/sign/add"
    data = {"ie": "utf-8", "kw": kw}
    try:
        res = session.post(url, data=data, timeout=10).json()
        no = res.get("no")
        msg = res.get("msg", "未知")
        if no == 0:
            return f"✅ {kw} → 签到成功"
        elif no == 1101:
            return f"✅ {kw} → 今日已签"
        else:
            return f"❌ {kw} → {msg}"
    except Exception as e:
        return f"⚠️ {kw} → 失败"

# ===================== 执行 =====================
if __name__ == "__main__":
    print("🚀 获取关注贴吧中...")
    tieba_list = get_like_tieba()

    if not tieba_list:
        print("❌ 获取失败，请重新抓Cookie")
        exit(1)

    print(f"🎯 共找到 {len(tieba_list)} 个贴吧\n")

    for i, name in enumerate(tieba_list, 1):
        print(f"{i}. {sign(name)}")
        time.sleep(1)

    print("\n🎉 签到任务全部完成！")
