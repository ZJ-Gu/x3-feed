#!/usr/bin/env python3
"""生成阅星曈 X3「视界」RSS 源：道德经（公版书）。
每日轮换：按一年中的第几天把对应章节置顶，实现"每日一章"。
输出 rss.xml 到仓库根目录，由 GitHub Pages / jsDelivr 托管。"""
from xml.sax.saxutils import escape
from datetime import datetime, timedelta, timezone
import random
import json
import os
import re

BASE = "https://zj-gu.github.io/x3-feed"
CHAPTERS = [tuple(x) for x in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "chapters.json"), encoding="utf-8"))]
CN = timezone(timedelta(hours=8))

def build_rss():
    now = datetime.now(CN)
    n = len(CHAPTERS)
    # 每日随机：以当天日期为种子，同一天内顺序固定，每天重新洗牌
    order = list(CHAPTERS)
    random.Random(now.strftime("%Y%m%d")).shuffle(order)
    order = order[:10]  # 视界卡片轻量展示，每天随机 10 章
    items = []
    for k, (t, body) in enumerate(order):
        orig_i = CHAPTERS.index((t, body)) + 1
        # 目录标题带首句名句，如「第19章 · 绝圣弃智，民利百倍」
        first = re.split(r"[。；]", body)[0]
        if len(first) > 16:  # 太长时在逗号/顿号处断，不拦腰砍词
            cut = max(first.rfind("，", 0, 17), first.rfind("、", 0, 17))
            first = first[:cut] if cut >= 6 else first[:16]
        dt = (now - timedelta(hours=k)).strftime("%a, %d %b %Y %H:%M:%S +0800")
        items.append(
            f"<item><title>第{orig_i}章 · {escape(first)}</title>"
            f"<description>{escape(body)}</description>"
            f"<link>{BASE}/#chapter-{orig_i}</link>"
            f"<guid isPermaLink=\"false\">ddj-{orig_i}-{now.strftime('%Y%m%d')}</guid>"
            f"<pubDate>{dt}</pubDate></item>"
        )
    intro = ("《道德经》每日轮播：道经三十七章、德经四十四章，凡八十一章。"
             "每日零点从全书中随机撷取十章，经文原文，常读常新。")
    return ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
            "<rss version=\"2.0\"><channel>"
            "<title>道德经</title>"
            f"<link>{BASE}/</link>"
            f"<description>{escape(intro)}</description>"
            "<language>zh-cn</language>"
            + "".join(items) + "</channel></rss>")

if __name__ == "__main__":
    out = build_rss()
    with open("rss.xml", "w", encoding="utf-8") as f:
        f.write(out)
    daily = list(CHAPTERS)
    random.Random(datetime.now(CN).strftime("%Y%m%d")).shuffle(daily)
    print("rss.xml written, 10/", len(CHAPTERS), "items, 今日随机置顶:", daily[0][0])
