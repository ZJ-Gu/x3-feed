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
    # 每日随机一章：以当天日期为种子
    order = list(CHAPTERS)
    random.Random(now.strftime("%Y%m%d")).shuffle(order)
    order = order[:1]
    items = []
    for k, (t, body) in enumerate(order):
        orig_i = CHAPTERS.index((t, body)) + 1
        img_url = f"{BASE}/wallpapers/ddj_{orig_i:02d}.jpg"
        dt = now.strftime("%a, %d %b %Y %H:%M:%S +0800")
        items.append(
            f"<item><title>今日一章 · 第{orig_i}章</title>"
            f"<description><![CDATA[<img src=\"{img_url}\"/><p>{body}</p>]]></description>"
            f"<enclosure url=\"{img_url}\" type=\"image/jpeg\" length=\"0\"/>"
            f"<media:content url=\"{img_url}\" type=\"image/jpeg\" medium=\"image\"/>"
            f"<link>{BASE}/wallpapers/ddj_{orig_i:02d}.jpg</link>"
            f"<guid isPermaLink=\"false\">ddj-{orig_i}-{now.strftime('%Y%m%d')}</guid>"
            f"<pubDate>{dt}</pubDate></item>"
        )
    intro = "《道德经》每日一章：每天零点从八十一章中随机撷取一章，竖排大字，常读常新。"
    return ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
            "<rss version=\"2.0\" xmlns:media=\"http://search.yahoo.com/mrss/\"><channel>"
            "<title>道德经 · 每日一章</title>"
            f"<link>{BASE}/</link>"
            f"<description>{escape(intro)}</description>"
            "<language>zh-cn</language>"
            + "".join(items) + "</channel></rss>")

if __name__ == "__main__":
    out = build_rss()
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rss.xml")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out)
    daily = list(CHAPTERS)
    random.Random(datetime.now(CN).strftime("%Y%m%d")).shuffle(daily)
    print("rss.xml written, 1/81 item, 今日随机:", daily[0][0])
