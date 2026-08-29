import re
from pathlib import Path

# ── fill in the YouTube IDs here and re-run ──
# the ID is the part after /shorts/ or after v= in the URL
VIDEOS = {
 1: {'id': 'PUT_ID_HERE', 'kr': '왕의 길목', 'en': "The King's Path",
     'kr_file': 'tistory_ch1_blood_and_fog.html',  'en_file': 'en/ch1.html'},
 4: {'id': 'PUT_ID_HERE', 'kr': '물 아래',   'en': 'Beneath the Water',
     'kr_file': 'tistory_ch5_sea_and_bones.html',  'en_file': 'en/ch5.html'},
 6: {'id': 'PUT_ID_HERE', 'kr': '이어도',    'en': 'Ieodo',
     'kr_file': 'tistory_ch6_island_and_stars.html','en_file': 'en/ch6.html'},
 7: {'id': 'PUT_ID_HERE', 'kr': '모루',      'en': 'The Anvil',
     'kr_file': 'chapter7.html',                    'en_file': 'en/chapter7.html'},
}


def block(vid, label, kr):
    return f'''<div class="filmwrap">
  <p class="label">{'영상' if kr else 'FILM'} · {label}</p>
  <div class="frame">
    <iframe src="https://www.youtube.com/embed/{vid}" title="{label}"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
      allowfullscreen loading="lazy"></iframe>
  </div>
</div>

'''


FILM_CSS = '''
  /* ---------- video embed ---------- */
  .filmwrap{ max-width:680px; margin:0 auto 40px; padding:0 24px; }
  .filmwrap .label{
    font-family:"Gowun Dodum", sans-serif; font-size:11px;
    letter-spacing:.28em; color:#7d8ba6; margin:0 0 14px; text-align:center;
  }
  .filmwrap .frame{
    position:relative; width:100%; max-width:330px; margin:0 auto;
    aspect-ratio:9/16; background:#0b1018;
    border:1px solid rgba(143,158,186,.16);
  }
  .filmwrap .frame iframe{ position:absolute; inset:0; width:100%; height:100%; border:0; }
'''

added = 0
for n, v in VIDEOS.items():
    if v['id'] == 'PUT_ID_HERE' or not v['id']:
        continue
    for path, kr, label in ((v['kr_file'], True, v['kr']), (v['en_file'], False, v['en'])):
        p = Path(path)
        if not p.exists():
            print('missing', path); continue
        s = p.read_text(encoding='utf-8')
        if 'filmwrap' in s:
            print(path, 'already has a film'); continue
        if '.filmwrap{' not in s:
            s = s.replace('</style>', FILM_CSS + '\n</style>', 1)
        blk = block(v['id'], label, kr)
        if '<article class="paper">' in s:
            s = s.replace('<article class="paper">', blk + '<article class="paper">', 1)
        elif '<div class="soonpage">' in s:
            s = s.replace('<div class="soonpage">', blk + '<div class="soonpage">', 1)
        else:
            print(path, 'no insertion point'); continue
        p.write_text(s, encoding='utf-8')
        added += 1
        print('film added ->', path)

if added == 0:
    print("\nNo videos added — the IDs are still placeholders.")
    print("Open this script, paste the YouTube IDs into VIDEOS, and run it again:")
    print("    python3 build_videos.py")
else:
    print(f"\n{added} embed(s) added.")
