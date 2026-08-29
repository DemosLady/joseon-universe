"""
generate_playlist_video.py
A 16:9 playlist video in the visual language of the albums: the panorama behind
everything, the cover of whatever album is playing on the left, the full
tracklist on the right coloured by trilogy, and the current track lit up.

SETUP
  1. tracklist.txt      start | korean | english | album number
  2. playlist.mp3       the audio, next to this script
  3. covers/ch1.jpg ... covers/ch8.jpg
  4. art/hero.jpg       the panorama
  5. art/mark.png       optional, the seal
  6. python generate_playlist_video.py

    --check          validate the tracklist and print it
    --preview 20     render one track so you can look at it
    --frames-only    render every still, skip the assembly

Needs pillow, and ffmpeg on PATH for the assembly step.
"""

import argparse, subprocess, sys, shutil
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
except ImportError:
    sys.exit("[ERROR] pillow is missing.  pip install pillow")

BASE = Path(__file__).parent
FRAMES = BASE / "playlist_frames"
TRACKLIST = BASE / "tracklist.txt"
BG_IMAGE = BASE / "art" / "hero.jpg"
MARK = BASE / "art" / "mark.png"
COVERS = BASE / "covers"

W, H = 1920, 1080

INK_TOP = (27, 36, 54)
INK_BOTTOM = (7, 11, 20)
BRIGHT = (240, 245, 252)
DIM = (128, 142, 168)
FAINT = (88, 100, 124)
RULE = (52, 64, 86)

TRILOGY = {
    "fire": {"albums": (1, 2, 3), "accent": (168, 105, 92),
             "kr": "불의 삼부작", "en": "THE FIRE TRILOGY"},
    "sea": {"albums": (4, 5, 6), "accent": (111, 163, 173),
            "kr": "바다 삼부작", "en": "THE SEA TRILOGY"},
    "iron": {"albums": (7, 8, 9), "accent": (150, 164, 184),
             "kr": "쇠 삼부작", "en": "THE IRON TRILOGY"},
}

ALBUM_NAMES = {
    1: ("피와 안개", "Blood and Fog"),
    2: ("먹과 불씨", "Ink and Embers"),
    3: ("재와 씨앗", "Ash and Seed"),
    4: ("소금과 파도", "Salt and Waves"),
    5: ("바다와 뼈", "Sea and Bones"),
    6: ("섬과 별", "Island and Stars"),
    7: ("눈과 쇠", "Snow and Iron"),
    8: ("쇠와 피", "Iron and Blood"),
    9: ("봄과 녹", "Spring and Rust"),
}

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\malgun.ttf",
    r"C:\Windows\Fonts\NanumMyeongjo.ttf",
    r"C:\Windows\Fonts\batang.ttc",
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]
FONT_BOLD = [r"C:\Windows\Fonts\malgunbd.ttf",
             r"C:\Windows\Fonts\NanumMyeongjoBold.ttf"] + FONT_CANDIDATES


def load_font(size, bold=False):
    for path in (FONT_BOLD if bold else FONT_CANDIDATES):
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    print("[warn] no Korean font found - text will render as boxes.")
    return ImageFont.load_default()


def trilogy_of(album):
    for key, t in TRILOGY.items():
        if album in t["albums"]:
            return key, t
    return "iron", TRILOGY["iron"]


SAMPLE = """# tracklist.txt
# One track per line:   start | korean title | english title | album number
# Times are where the track STARTS, as mm:ss or h:mm:ss.
# The album number picks the cover and the trilogy colour.
# End with a line giving the finish time and the word END.

00:00 | 왕의 길목 | The King's Path | 1
03:12 | 빈 궁궐 메아리 | Echoes of the Empty Palace | 1

1:47:00 | END
"""


def parse_time(s):
    parts = [int(p) for p in s.strip().split(":")]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    raise ValueError(f"bad time: {s}")


def read_tracklist():
    if not TRACKLIST.exists():
        TRACKLIST.write_text(SAMPLE, encoding="utf-8")
        print(f"[created] {TRACKLIST}\nFill it in and run again.")
        sys.exit(0)

    rows = []
    for ln in TRACKLIST.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        p = [x.strip() for x in ln.split("|")]
        rows.append((parse_time(p[0]),
                     p[1] if len(p) > 1 else "",
                     p[2] if len(p) > 2 else "",
                     int(p[3]) if len(p) > 3 and p[3].isdigit() else 1))

    tracks = []
    for i, (t, kr, en, al) in enumerate(rows):
        if not kr or kr.upper() == "END":
            break
        if i + 1 >= len(rows):
            sys.exit("[ERROR] the last track has no end time - add a final END line")
        tracks.append({"n": i + 1, "start": t, "end": rows[i + 1][0],
                       "kr": kr, "en": en, "album": al})
    if not tracks:
        sys.exit("[ERROR] no tracks found")
    return tracks



def durations_from_folder(folder: Path):
    """Read the length of every audio file in a folder, in filename order.
    Needs ffprobe, which ships with ffmpeg."""
    if not folder.exists():
        return None
    exts = (".mp3", ".wav", ".m4a", ".flac", ".aac", ".ogg")
    files = sorted([f for f in folder.iterdir() if f.suffix.lower() in exts])
    if not files:
        return None
    if not shutil.which("ffprobe"):
        print("[note] ffprobe not on PATH — cannot read durations automatically")
        return None
    out = []
    for f in files:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(f)],
            capture_output=True, text=True)
        try:
            out.append((f.name, float(r.stdout.strip())))
        except ValueError:
            print(f"[note] could not read {f.name}")
            return None
    return out


def fill_times_from_audio(tracks, folder: Path):
    """Overwrite the start/end times using the real file lengths."""
    durs = durations_from_folder(folder)
    if durs is None:
        return False
    if len(durs) != len(tracks):
        print(f"[note] {len(durs)} audio files but {len(tracks)} tracks — "
              f"leaving the times in tracklist.txt alone")
        return False
    t = 0
    for track, (name, dur) in zip(tracks, durs):
        track["start"] = int(round(t))
        t += dur
        track["end"] = int(round(t))
        track["file"] = name
    return True


def make_background():
    bg = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(bg)
    for y in range(H):
        f = (y / H) ** 0.85
        d.line([(0, y), (W, y)],
               fill=tuple(int(INK_TOP[i] + (INK_BOTTOM[i] - INK_TOP[i]) * f) for i in range(3)))

    if BG_IMAGE.exists():
        pano = Image.open(BG_IMAGE).convert("RGB")
        r = max(W / pano.width, H / pano.height)
        pano = pano.resize((int(pano.width * r), int(pano.height * r)), Image.LANCZOS)
        l = (pano.width - W) // 2
        t = int((pano.height - H) * 0.42)
        pano = pano.crop((l, t, l + W, t + H)).filter(ImageFilter.GaussianBlur(3))
        pano = ImageEnhance.Color(pano).enhance(0.5)
        bg = Image.blend(bg, pano, 0.13)
    else:
        print("[note] art/hero.jpg not found - plain gradient")

    vig = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vig).ellipse([-W // 3, -H // 2, W + W // 3, H + H // 2], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(220))
    return Image.composite(bg, ImageEnhance.Brightness(bg).enhance(0.62), vig)


def load_cover(album, size):
    for ext in ("jpg", "jpeg", "png"):
        p = COVERS / f"ch{album}.{ext}"
        if p.exists():
            im = Image.open(p).convert("RGB")
            s = min(im.size)
            im = im.crop(((im.width - s) // 2, (im.height - s) // 2,
                          (im.width + s) // 2, (im.height + s) // 2))
            return im.resize((size, size), Image.LANCZOS)
    return None


def render(tracks, cur, bg, fonts, covers):
    f_tr, f_num, f_en, f_head, f_sub, f_alb, f_albsub, f_lbl = fonts
    img = bg.copy().convert("RGBA")
    over = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(over)
    d = ImageDraw.Draw(img)

    track = next(t for t in tracks if t["n"] == cur)
    _, tri = trilogy_of(track["album"])
    accent = tri["accent"]

    d.text((W // 2, 58), "조선 이야기", font=f_head, fill=BRIGHT, anchor="mm")
    d.text((W // 2, 104), "J O S E O N   S T O R I E S   ·   d e m o s a i i",
           font=f_sub, fill=FAINT, anchor="mm")
    d.line([(W // 2 - 340, 138), (W // 2 + 340, 138)], fill=RULE, width=1)

    CS, cx, cy = 380, 128, 214
    cov = covers.get(track["album"])
    if cov is not None:
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rectangle([cx + 8, cy + 14, cx + CS + 8, cy + CS + 14],
                                     fill=(0, 0, 0, 150))
        over.alpha_composite(sh.filter(ImageFilter.GaussianBlur(22)))
        img.paste(cov, (cx, cy))
        d.rectangle([cx, cy, cx + CS, cy + CS], outline=(255, 255, 255), width=1)
    else:
        d.rectangle([cx, cy, cx + CS, cy + CS], outline=RULE, width=1)

    ak, ae = ALBUM_NAMES.get(track["album"], ("", ""))
    ty = cy + CS + 46
    od.rectangle([cx, ty - 22, cx + 46, ty - 20], fill=accent + (230,))
    d.text((cx, ty + 14), ak, font=f_alb, fill=BRIGHT, anchor="lm")
    d.text((cx, ty + 52), ae.upper(), font=f_albsub, fill=DIM, anchor="lm")
    d.text((cx, ty + 90), f"{tri['kr']}  ·  {tri['en']}", font=f_lbl, fill=accent, anchor="lm")

    if MARK.exists():
        m = Image.open(MARK).convert("RGBA").resize((92, 92), Image.LANCZOS)
        m.putalpha(m.split()[-1].point(lambda v: int(v * 0.5)))
        over.alpha_composite(m, (cx, H - 172))

    od.line([(578, 200), (578, H - 116)], fill=RULE + (150,), width=1)

    n = len(tracks)
    cols = 2 if n > 15 else 1
    per_col = (n + 1) // 2 if n > 15 else n
    top, bottom = 196, H - 108
    row_h = (bottom - top) // per_col
    left = 648
    col_w = (W - left - 90) // cols

    for i, t in enumerate(tracks):
        c, r = i // per_col, i % per_col
        x = left + c * col_w
        y = top + r * row_h + row_h // 2
        _, ttri = trilogy_of(t["album"])
        now = (t["n"] == cur)

        if now:
            od.rectangle([x - 40, y - row_h // 2 + 2, x + col_w - 66, y + row_h // 2 - 2],
                         fill=(255, 255, 255, 15))
            od.rectangle([x - 40, y - row_h // 2 + 2, x - 37, y + row_h // 2 - 2],
                         fill=accent + (240,))
            c_kr, c_en, c_no = BRIGHT, DIM, accent
        else:
            c_kr, c_en = DIM, FAINT
            c_no = tuple(int(FAINT[k] * 0.6 + ttri["accent"][k] * 0.4) for k in range(3))

        d.text((x, y - 9), f"{t['n']:02d}", font=f_num, fill=c_no, anchor="lm")
        d.text((x + 52, y - 9), t["kr"], font=f_tr, fill=c_kr, anchor="lm")
        if t["en"]:
            d.text((x + 52, y + 16), t["en"], font=f_en, fill=c_en, anchor="lm")

    img = Image.alpha_composite(img, over).convert("RGB")
    ImageDraw.Draw(img).text((W // 2, H - 46), "joseon-universe.vercel.app",
                             font=f_sub, fill=FAINT, anchor="mm")
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames-only", action="store_true")
    ap.add_argument("--preview", type=int)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--audio", default="playlist.mp3")
    ap.add_argument("--out", default="playlist_video.mp4")
    ap.add_argument("--tracks", default="tracks",
                    help="folder of individual audio files; if present, "
                         "durations are read from them and the times in "
                         "tracklist.txt are ignored")
    args = ap.parse_args()

    tracks = read_tracklist()

    auto = fill_times_from_audio(tracks, BASE / args.tracks)
    if auto:
        print(f"\n[auto] times read from {args.tracks}/ — tracklist.txt times ignored")

    total = tracks[-1]["end"]
    print(f"\n{len(tracks)} tracks  ·  {total//3600}:{(total%3600)//60:02d}:{total%60:02d}\n")
    for t in tracks:
        dur = t["end"] - t["start"]
        print(f"  {t['n']:02d}  album {t['album']}  {t['start']//60:>3}:{t['start']%60:02d}"
              f"  ({dur//60}:{dur%60:02d})  {t['kr']}")
    if args.check:
        return

    FRAMES.mkdir(exist_ok=True)
    bg = make_background()
    covers = {a: load_cover(a, 380) for a in sorted({t["album"] for t in tracks})}
    missing = [a for a, c in covers.items() if c is None]
    if missing:
        print(f"\n[note] no cover found for album(s): {missing}")

    fonts = (load_font(25), load_font(17), load_font(14), load_font(42, bold=True),
             load_font(15), load_font(31, bold=True), load_font(15), load_font(14))

    todo = [t for t in tracks if (args.preview is None or t["n"] == args.preview)]
    print()
    for t in todo:
        render(tracks, t["n"], bg, fonts, covers).save(FRAMES / f"track_{t['n']:02d}.png")
        print(f"  rendered track_{t['n']:02d}.png")

    if args.preview:
        print(f"\nopen {FRAMES}")
        return
    if args.frames_only:
        print(f"\n{len(todo)} frame(s) in {FRAMES}")
        return

    if not shutil.which("ffmpeg"):
        print("\nffmpeg not on PATH - frames are ready, assemble them yourself.")
        return
    audio = BASE / args.audio
    if not audio.exists() and auto:
        print(f"\n{args.audio} not found — joining the files in {args.tracks}/ instead")
        alist = BASE / "_audio.txt"
        folder = BASE / args.tracks
        exts = (".mp3", ".wav", ".m4a", ".flac", ".aac", ".ogg")
        files = sorted([f for f in folder.iterdir() if f.suffix.lower() in exts])
        alist.write_text("\n".join(f"file '{f.as_posix()}'" for f in files), encoding="utf-8")
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(alist),
                        "-c:a", "libmp3lame", "-b:a", "256k", str(audio)], check=False)
        alist.unlink(missing_ok=True)
    if not audio.exists():
        print(f"\naudio not found: {audio}\nframes are ready.")
        return

    concat = BASE / "_concat.txt"
    lines = []
    for t in tracks:
        lines.append(f"file '{(FRAMES / ('track_%02d.png' % t['n'])).as_posix()}'")
        lines.append(f"duration {t['end'] - t['start']}")
    lines.append(f"file '{(FRAMES / ('track_%02d.png' % tracks[-1]['n'])).as_posix()}'")
    concat.write_text("\n".join(lines), encoding="utf-8")

    out = BASE / args.out
    print(f"\nassembling {out.name} - this takes a while\n")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
                    "-i", str(audio), "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-r", "2", "-c:a", "aac", "-b:a", "256k",
                    "-shortest", str(out)], check=False)
    concat.unlink(missing_ok=True)
    print(f"\ndone -> {out}")


if __name__ == "__main__":
    main()
