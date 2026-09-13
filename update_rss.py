# -*- coding: utf-8 -*-
"""Adds one entry to the top of rss.xml. Run it whenever something new goes up.

    python update_rss.py "제10장 · 새 이야기" chapter10.html "한 줄 설명"
"""
import sys, re
from pathlib import Path
from email.utils import format_datetime
from datetime import datetime, timezone, timedelta

B = "https://joseon-universe.com"
KST = timezone(timedelta(hours=9))

if len(sys.argv) < 3:
    sys.exit(__doc__)

title, page = sys.argv[1], sys.argv[2].lstrip("/")
desc = sys.argv[3] if len(sys.argv) > 3 else ""
esc = lambda x: x.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
now = format_datetime(datetime.now(KST))

p = Path(__file__).parent / "rss.xml"
s = p.read_text(encoding="utf-8")
if f"{B}/{page}<" in s:
    sys.exit(f"{page} is already in the feed")

item = f"""    <item>
      <title>{esc(title)}</title>
      <link>{B}/{page}</link>
      <guid isPermaLink="true">{B}/{page}</guid>
      <pubDate>{now}</pubDate>
      <category>조선 이야기</category>
      <description>{esc(desc)}</description>
    </item>
"""
s = re.sub(r"(<lastBuildDate>)[^<]*(</lastBuildDate>)", r"\g<1>" + now + r"\g<2>", s, count=1)
s = s.replace("    <item>", item + "    <item>", 1)
p.write_text(s, encoding="utf-8")
print(f"added: {title}\nitems now: {s.count('<item>')}")
