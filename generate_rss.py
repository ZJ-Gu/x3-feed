#!/usr/bin/env python3
"""生成阅星曈 X3「视界」RSS 源：道德经（公版书）。
每日轮换：按一年中的第几天把对应章节置顶，实现"每日一章"。
输出 rss.xml 到仓库根目录，由 GitHub Pages / jsDelivr 托管。"""
from xml.sax.saxutils import escape
from datetime import datetime, timedelta, timezone
import random

BASE = "https://zj-gu.github.io/x3-feed"
CHAPTERS = [
    ("第一章", "道可道，非常道；名可名，非常名。无名天地之始，有名万物之母。故常无欲，以观其妙；常有欲，以观其徼。此两者同出而异名，同谓之玄，玄之又玄，众妙之门。"),
    ("第二章", "天下皆知美之为美，斯恶已；皆知善之为善，斯不善已。故有无相生，难易相成，长短相形，高下相倾，音声相和，前后相随。是以圣人处无为之事，行不言之教，万物作焉而不辞，生而不有，为而不恃，功成而弗居。夫唯弗居，是以不去。"),
    ("第三章", "不尚贤，使民不争；不贵难得之货，使民不为盗；不见可欲，使民心不乱。是以圣人之治，虚其心，实其腹；弱其志，强其骨。常使民无知无欲，使夫智者不敢为也。为无为，则无不治。"),
    ("第四章", "道冲而用之或不盈，渊兮似万物之宗。挫其锐，解其纷，和其光，同其尘。湛兮似或存，吾不知谁之子，象帝之先。"),
    ("第五章", "天地不仁，以万物为刍狗；圣人不仁，以百姓为刍狗。天地之间，其犹橐籥乎？虚而不屈，动而愈出。多言数穷，不如守中。"),
    ("第六章", "谷神不死，是谓玄牝。玄牝之门，是谓天地根。绵绵若存，用之不勤。"),
    ("第七章", "天长地久。天地所以能长且久者，以其不自生，故能长生。是以圣人后其身而身先，外其身而身存。非以其无私邪？故能成其私。"),
    ("第八章", "上善若水。水善利万物而不争，处众人之所恶，故几于道。居善地，心善渊，与善仁，言善信，正善治，事善能，动善时。夫唯不争，故无尤。"),
    ("第九章", "持而盈之，不如其已；揣而锐之，不可长保。金玉满堂，莫之能守；富贵而骄，自遗其咎。功遂身退，天之道。"),
]
CN = timezone(timedelta(hours=8))

def build_rss():
    now = datetime.now(CN)
    n = len(CHAPTERS)
    # 每日随机：以当天日期为种子，同一天内顺序固定，每天重新洗牌
    order = list(CHAPTERS)
    random.Random(now.strftime("%Y%m%d")).shuffle(order)
    items = []
    for k, (t, body) in enumerate(order):
        orig_i = CHAPTERS.index((t, body)) + 1
        dt = (now - timedelta(hours=k)).strftime("%a, %d %b %Y %H:%M:%S +0800")
        items.append(
            f"<item><title>道德经 · {escape(t)}</title>"
            f"<description>{escape(body)}</description>"
            f"<link>{BASE}/#chapter-{orig_i}</link>"
            f"<guid isPermaLink=\"false\">ddj-{orig_i}-{now.strftime('%Y%m%d')}</guid>"
            f"<pubDate>{dt}</pubDate></item>"
        )
    return ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
            "<rss version=\"2.0\"><channel>"
            "<title>道德经 · 每日轮播</title>"
            f"<link>{BASE}/</link>"
            "<description>阅星曈 X3 视界订阅源（公版内容）</description>"
            "<language>zh-cn</language>"
            + "".join(items) + "</channel></rss>")

if __name__ == "__main__":
    out = build_rss()
    with open("rss.xml", "w", encoding="utf-8") as f:
        f.write(out)
    daily = list(CHAPTERS)
    random.Random(datetime.now(CN).strftime("%Y%m%d")).shuffle(daily)
    print("rss.xml written,", len(CHAPTERS), "items, 今日随机置顶:", daily[0][0])
