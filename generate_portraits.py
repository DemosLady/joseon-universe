"""
generate_portraits.py
Builds one portrait per character for the characters page.

    python generate_portraits.py                all ten, skips existing
    python generate_portraits.py --only oki     one character
    python generate_portraits.py --limit 3      first three missing
    python generate_portraits.py --force        regenerate

Output: portraits/king.jpg, portraits/yeoni.jpg ... matching the anchor ids
already used on characters.html, so the page can pick them up directly.
"""

import os, sys, time, base64, argparse
from pathlib import Path

import requests
from dotenv import load_dotenv

BASE = Path(__file__).parent
load_dotenv(BASE.parent / ".env")

NANO_KEY = os.getenv("NANO_KEY")
NB_MODEL = os.getenv("NB_MODEL")
if not NANO_KEY or not NB_MODEL:
    sys.exit(f"[ERROR] NANO_KEY / NB_MODEL not found in {BASE.parent / '.env'}")

URL = (f"https://generativelanguage.googleapis.com/v1beta/models/"
       f"{NB_MODEL}:generateContent?key={NANO_KEY}")

OUT = BASE / "portraits"
OUT.mkdir(exist_ok=True)

REFS = BASE / "refs"          # optional: refs/king.png locks a face you already have
REFS.mkdir(exist_ok=True)


# ── the shared formula ────────────────────────────────────────────────────────
# Byte-identical on every portrait. Change it here or not at all — any wording
# drift between characters and they stop looking like one series.

HEAD = ("Cinematic Korean historical drama portrait, vertical 4:5, photographic. ")

TAIL = (" Shot on a long lens at a wide aperture so only the face is sharp and the "
        "background falls away immediately into soft darkness. Restrained muted "
        "palette, fine film grain, natural photographic falloff. The subject looks "
        "directly into the camera, level and unblinking, not posed and not smiling. "
        "No glow, no aura, no lens flares, no text, no watermark, no modern objects, "
        "no Chinese or Japanese dress, no anime or illustration style, no CGI sheen, "
        "no theatrical or exaggerated expression, no jewellery unless described. "
        "AGE LOCK: depict the subject at exactly the stated age and no older. Do "
        "not add grey hair, sagging skin, heavy jowls or deep folds that were not "
        "described. Weathering means sun and wind on otherwise firm skin, not old "
        "age. All subjects are unmistakably Korean in facial structure. "
        "Portrait orientation, taller than wide, camera upright and level, never "
        "tilted, never rotated, never landscape.")


CHARACTERS = [
 ("king", "왕 · The King",
  "A Korean man of EXACTLY thirty-two years old in a dark palace hall, wearing a crimson red silk "
  "gonryongpo robe with a circular gold-embroidered dragon roundel at the chest and a "
  "white inner collar, and on his head the ikseongwan, a black lacquered gauze crown with "
  "two small wings standing upright and vertical from the back of it, pointing up, never "
  "flat or sideways. Pale indoor skin, a thin neatly kept beard, tired shadows beneath the "
  "eyes, his expression closed and heavy with something unsaid. Lit warm and low from one "
  "side by a single oil lamp and cold from the other by moonlight, deep black between them."),

 ("yeoni", "연이 · Yeon-i",
  "A Korean woman of EXACTLY twenty-six years old, unmistakably Korean, in a dark palace room, wearing a plain pale jade-green "
  "silk jeogori jacket over a soft white skirt, her black hair drawn back simply with a "
  "single plain hairpin and no ornament at all. A calm unadorned face, no cosmetics, a "
  "stillness about her as though she is listening to something outside the room. Lit only by "
  "cold moonlight through a paper door, the light falling across one side of her face and "
  "the rest lost in shadow."),

 ("yunje", "윤제 · Yun-je",
  "A Korean man of EXACTLY thirty-eight years old, a scholar, wearing a plain undyed white hemp durumagi "
  "robe worn thin and mended at the collar, his black hair in a topknot with no gat hat. A "
  "lean intelligent face, salt-dried skin darkened by years of sea wind and sun, ink "
  "permanently staining the fingers of one hand visible at the edge of frame. Lit by weak "
  "daylight from a low window, the sea out of focus far behind him."),

 ("talswe", "탈쇠 · Tal-swe",
  "A Korean man of EXACTLY thirty-four years old, a market entertainer, wearing a patched hemp jacket in "
  "mismatched faded colours tied with a rope belt, a cloth headband, no hat. A quick mobile "
  "face with laughter lines that do not reach the eyes, a small old scar through one "
  "eyebrow. He holds a carved wooden mask loosely at his side, lowered, not worn and not "
  "covering his face. Lit by warm afternoon market light with the blurred movement of a "
  "crowd behind him."),

 ("jeongan", "정안 · Jeong-an",
  "A Korean woman of EXACTLY forty-three years old with a shaved head, wearing a plain grey "
  "Buddhist monastic robe. Her face is still firm and unlined except at the corners of the "
  "eyes, the skin clear, the jaw defined, a strong-boned face that is composed rather than "
  "aged. She is a woman in her early forties and must not read as older, not sixty, not "
  "elderly. An old shiny burn scar runs across the back of one hand resting near her chest. "
  "Lit by flat cold light from an open temple door, the mountain out of focus behind her."),

 ("buni_young", "분이 (16세) · Bun-i at sixteen",
  "A Korean GIRL of EXACTLY sixteen years old, an adolescent and not an adult woman, in "
  "plain undyed hemp village clothing, worn and mended, her black hair in a single simple "
  "braid. Her face still has the proportions of a teenager: large eyes set wide in a small "
  "face, a soft undefined jawline, rounded cheeks with baby fat still present, a short "
  "nose, thin unshaped eyebrows, and completely smooth skin with no lines anywhere at all, "
  "only a light tan from field work. Her frame is slight and narrow-shouldered, not yet "
  "fully grown. She is fifteen or sixteen, the same age as a middle school student. Her "
  "expression is serious and stubbornly determined rather than sweet. She must read "
  "unmistakably as a teenager and NOT as a woman in her twenties or thirties. Lit by plain "
  "daylight from one side in a bare village room, a wooden floor out of focus behind her."),

 ("buni", "분이 (44세) · Bun-i at forty-four",
  "A Korean woman of EXACTLY forty-four years old in plain undyed hemp village clothing, her "
  "black hair tied back simply under a cloth headband with no grey in it. Her face is firm and "
  "smooth with only faint lines at the corners of the eyes, lightly sun-darkened, a plain steady "
  "face in early middle age. She must not read as elderly or as sixty. Ink stains on the first "
  "two fingers of the hand she holds near her chest. Lit by daylight from one side in a bare "
  "village room, a low writing table out of focus behind her."),

 ("sugyeom", "수겸 · Su-gyeom",
  "A Korean man of EXACTLY forty-two years old in undyed white hemp, thin and worn, with a rope belt, "
  "his black hair in a topknot with no hat. A gaunt refined face burned by sun and salt, "
  "cracked lips, ink on his fingers. Lit by hard bright daylight bouncing up off water, the "
  "open sea thrown far out of focus behind him."),

 ("baeswe", "배쇠 · Bae-swe",
  "A Korean man of EXACTLY fifty-four years old, weather-beaten and solidly built but not fat, wearing dark undyed hemp with "
  "the sleeves cut short at the elbow and a coarse rope belt, a dark cloth wrapped around "
  "his head. A hard closed face with deep sun lines and a broken nose, rope burns across the "
  "palms of the hands. Lit by low blue pre-dawn light on open water, the mast of a boat out "
  "of focus behind him."),

 ("gapsu", "갑수 · Gap-su",
  "A Korean man of EXACTLY sixty-eight years old, small and wiry, wearing a worn undyed hemp jacket over "
  "a plain inner robe, both faded and mended, a plain cloth headband over grey hair in a low "
  "topknot. A deeply lined face, eyes narrowed permanently from decades of glare off the "
  "sea, enormous thick-knuckled hands. Lit by soft grey overcast daylight, a fishing net out "
  "of focus behind him."),

 ("oki", "옥이 · Ok-i",
  "A Korean woman of EXACTLY thirty-five years old, unmistakably Korean in facial structure, "
  "wearing a sleeveless undyed off-white cotton haenyeo diving top with bare shoulders and "
  "bare arms and a plain off-white cotton headband tied at the back of her head. She is LEAN "
  "and MUSCULAR from a lifetime of diving and rowing, with a narrow face, defined jaw and "
  "visible tendons in the neck and forearms, never heavy-set, never soft, never round-faced. "
  "Sun-darkened skin with freckles across the nose and fine lines at the eyes, wet black hair "
  "pulled back, water still on her skin. Lit by hard bright daylight off the sea, the water "
  "thrown far out of focus behind her."),
]


def find_ref(cid: str):
    for ext in ("png", "jpg", "jpeg", "webp"):
        f = REFS / f"{cid}.{ext}"
        if f.exists():
            return f
    return None


def call_gemini(prompt: str, ref: Path | None):
    parts = []
    if ref:
        mime = "image/png" if ref.suffix.lower() == ".png" else "image/jpeg"
        parts.append({"text":
            "IDENTITY REFERENCE — THIS IS THE PERSON. The photograph below shows the exact "
            "human being you must depict. Reproduce this face precisely: the same age, the "
            "same bone structure, the same nose and mouth, the same eyes, the same skin "
            "including every freckle, line and blemish. Do NOT beautify, do NOT make them "
            "younger, thinner or smoother. Do not copy the framing, the crop, the clothing "
            "or the lighting from this photograph — only the person. Reference photograph:"})
        parts.append({"inline_data": {
            "mime_type": mime,
            "data": base64.b64encode(ref.read_bytes()).decode()}})
    parts.append({"text": prompt})

    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "temperature": 0.1,
            "responseModalities": ["image", "text"],
            "imageConfig": {"aspectRatio": "4:5"},
        },
    }
    for attempt in range(1, 4):
        r = requests.post(URL, json=payload, timeout=300)
        if r.status_code == 429:
            print(f"      rate limited, sleeping 30s ({attempt}/3)")
            time.sleep(30)
            continue
        if r.status_code != 200:
            print(f"      HTTP {r.status_code}: {r.text[:250]}")
            return None
        rp = r.json().get("candidates", [{}])[0].get("content", {}).get("parts", [])
        b64 = next((p["inlineData"]["data"] for p in rp if "inlineData" in p), None)
        if b64:
            return base64.b64decode(b64)
        print("      no image in response")
        return None
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="single character id, e.g. oki")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--list", action="store_true", help="print the ids and exit")
    args = ap.parse_args()

    if args.list:
        for cid, label, _ in CHARACTERS:
            print(f"  {cid:<10} {label}")
        return

    rows = [c for c in CHARACTERS if (args.only is None or c[0] == args.only)]
    if not rows:
        sys.exit(f"no character called {args.only} — try --list")

    made = 0
    for cid, label, desc in rows:
        if args.limit and made >= args.limit:
            print("\nlimit reached.")
            break

        dest = OUT / f"{cid}.png"
        if dest.exists() and not args.force:
            print(f"[have] {cid}.png   {label}")
            continue

        ref = find_ref(cid)
        if ref:
            print(f"[gen ] {cid}.png   {label}")
            print(f"       USING REFERENCE: {ref}")
        else:
            print(f"[gen ] {cid}.png   {label}")
            print(f"       no reference found — looked for {REFS}/{cid}.png|jpg|jpeg|webp")

        img = call_gemini(HEAD + desc + TAIL, ref)
        if img:
            dest.write_bytes(img)
            print(f"       saved -> {dest}")
            made += 1
        else:
            print("       FAILED")
        time.sleep(2)

    print(f"\n{'=' * 62}")
    print(f"done. {made} portrait(s) in {OUT}")
    print("=" * 62)
    print("""
BEFORE YOU USE THEM
  Look at all ten side by side. They must read as ONE series — same lens, same
  restraint, same distance. If one is noticeably brighter, closer or more posed
  than the rest, regenerate that one:
      python generate_portraits.py --only talswe --force

TO LOCK A FACE YOU ALREADY HAVE
  Drop it in refs/ named after the id — refs/king.png — and run again with
  --force. The script will reproduce that exact face instead of inventing one.
  Useful for the king, whose portrait already exists from the video projects.

THEN
  Copy the portraits/ folder next to characters.html and tell me — I'll wire
  them into the page.
""")


if __name__ == "__main__":
    main()
