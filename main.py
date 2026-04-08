import os
import requests
import time

# ====================== 你的贴吧列表已填好 ======================
MY_TIEBA_LIST = """
qq飞车,炉石传说,bilibili,克鲁赛德战记,禹州一高,在的你收获幸福了吗,海贼王,暴走漫画,初音ミク,龙族,三体,河南大学,ps,笔记本,pr,minecraft,鼠标,机械键盘,c语言,图拉丁,xylon,四散的尘埃,雷霆战机,俄罗斯大神系统,赛尔号,宫漫,qq水浒,qq宠物,sdorica,云图计划,贴吧吧主,原神,核战避难所,天天酷跑,qq飞车游戏交流,看门狗2,novelai,steam,环行旅舍,原神内鬼,弱智,崩坏星穹铁道内鬼,玉足占领地球,随从大师,二次元小雷,大富翁,清朝,明朝
"""
# ==============================================================

cookie = os.getenv("TIEBA_COOKIE", "").strip()
if not cookie:
    print("❌ 未设置Cookie")
    exit(1)

headers = {
    "Cookie": cookie,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://tieba.baidu.com/"
}

tiebas = [x.strip() for x in MY_TIEBA_LIST.strip().split(",") if x.strip()]

def sign(kw):
    url = "https://tieba.baidu.com/sign/add"
    data = {"ie": "utf-8", "kw": kw}
    try:
        res = requests.post(url, data=data, headers=headers, timeout=10).json()
        no = res.get("no")
        if no == 0:
            return f"✅ {kw} 签到成功"
        elif no == 1101:
            return f"✅ {kw} 今日已签"
        else:
            return f"❌ {kw} 失败：{res.get('msg', '未知错误')}"
    except Exception as e:
        return f"⚠️ {kw} 请求异常"

if __name__ == "__main__":
    print("🚀 贴吧自动签到开始")
    print(f"🎯 共 {len(tiebas)} 个贴吧\n")

    for i, bar in enumerate(tiebas, 1):
        print(f"{i}. {sign(bar)}")
        time.sleep(1)

    print("\n🎉 全部签到完成！")
