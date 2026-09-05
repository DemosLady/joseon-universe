"""
generate_playlist_video.py  —  cover-flow edition, with rotating transitions

Renders one still per track, and optionally the in-between frames where the
carousel rotates from one track to the next.

SETUP
  1. tracklist.txt   start | korean | english | album no. | romanised title
  2. lyrics.txt      track no. | korean line | romanised line | english line
  3. covers/         01.jpg 02.jpg ...   (per track — preferred)
                     ch1.jpg ch2.jpg ... (per album — fallback, auto-cropped)
  4. art/mark.png    the seal, transparent PNG
  5. art/hero.jpg    optional, laid over the backdrop
  6. python generate_playlist_video.py

    --check              print the tracklist, render nothing
    --preview 3          one still, to check the layout
    --transitions        also render the rotation between every pair
    --fps 30             frames per second for the transitions
    --dur 0.5            seconds per transition
    --text fade|cut      how the lyric line and player bar change over
    --ease ease|smooth|linear

Needs pillow.  ffmpeg on PATH lets --transitions also write one short mp4
per transition, which is far easier to drop into an editor than a folder
of numbered stills.
"""

import argparse, subprocess, sys, shutil, math, random
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
except ImportError:
    sys.exit("[ERROR] pillow is missing.  pip install pillow")

BASE = Path(__file__).parent
FRAMES = BASE / "playlist_frames"
TRANS = BASE / "transitions"
TRACKLIST = BASE / "tracklist.txt"
LYRICS = BASE / "lyrics.txt"
BG_IMAGE = BASE / "art" / "hero.jpg"
MARK = BASE / "art" / "mark.png"
COVERS = BASE / "covers"

W, H = 1920, 1080

BRIGHT = (245, 248, 252)
DIM = (176, 190, 206)
BAR_FILL = (26, 26, 28)

# The backdrop follows the trilogy the current track belongs to, and cross
# fades when a transition crosses from one trilogy into the next.
BG_PALETTE = {
    "fire": ((112, 62, 48), (30, 14, 13)),
    "sea":  ((42, 106, 152), (14, 34, 56)),
    "iron": ((116, 128, 142), (26, 32, 42)),
}

# --- the artwork laid over the backdrop -------------------------------------
HERO_OPACITY = 0.55
HERO_BLUR = 0
HERO_SATURATION = 0.7
HERO_CLEAR_CENTRE = 0.55

# --- the compilation header -------------------------------------------------
COMP_TITLE_KR = "조선의 여자들"
COMP_TITLE_EN = "WOMEN OF JOSEON"
COMP_TAGLINE = ("Fourteen songs led by women, drawn from all eight EPs  ·  "
                "the ghost, the nun, the diver, the scribe")
BRUSH_WIDTH = 620

# --- youtube thumbnail ------------------------------------------------------
THUMB_LINE = "14 SONGS  ·  8 EPs  ·  ONE STORY"
THUMB_IMAGE = BASE / "art" / "thumb.jpg"   # falls back to covers/ch1

# --- transitions ------------------------------------------------------------
FPS = 30
TRANSITION_SECONDS = 0.5
EASING = "ease"        # ease | smooth | linear
TEXT_MODE = "fade"     # fade | cut

# Two tracks from the same EP would otherwise show the same picture; each
# repeat gets a different crop: (zoom, horizontal anchor, vertical anchor).
COVER_VARIANTS = [
    (1.00, 0.50, 0.50),
    (0.66, 0.22, 0.30),
    (0.66, 0.80, 0.66),
    (0.78, 0.50, 0.18),
]

# The colour a card takes on as it moves off centre.  Fixed per track, so a
# card keeps its identity while it rotates instead of changing hue mid-move.
SIDE_TINTS = [
    (150, 178, 190),
    (140, 96, 132),
    (198, 172, 140),
    (168, 178, 190),
]

TRILOGY = {
    "fire": {"albums": (1, 2, 3), "accent": (198, 118, 100),
             "kr": "불의 삼부작", "en": "THE FIRE TRILOGY"},
    "sea": {"albums": (4, 5, 6), "accent": (118, 176, 186),
            "kr": "바다 삼부작", "en": "THE SEA TRILOGY"},
    "iron": {"albums": (7, 8, 9), "accent": (166, 180, 198),
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

FONT_REG = [
    r"C:\Windows\Fonts\malgun.ttf",
    r"C:\Windows\Fonts\NanumMyeongjo.ttf",
    r"C:\Windows\Fonts\batang.ttc",
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]
FONT_BLD = [r"C:\Windows\Fonts\malgunbd.ttf",
            r"C:\Windows\Fonts\NanumMyeongjoBold.ttf",
            "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf"] + FONT_REG
FONT_ITA = [r"C:\Windows\Fonts\segoeuii.ttf",
            r"C:\Windows\Fonts\ariali.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"] + FONT_REG


def load_font(size, kind="reg"):
    table = {"reg": FONT_REG, "bold": FONT_BLD, "italic": FONT_ITA}[kind]
    for path in table:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    print("[warn] no suitable font found - text may render as boxes.")
    return ImageFont.load_default()


def trilogy_of(album):
    for key, t in TRILOGY.items():
        if album in t["albums"]:
            return key, t
    return "iron", TRILOGY["iron"]


# ---- easing ----------------------------------------------------------------
def ease(t, mode=None):
    mode = mode or EASING
    t = max(0.0, min(1.0, t))
    if mode == "linear":
        return t
    if mode == "smooth":
        return t * t * (3 - 2 * t)
    return 4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2


# ---- perspective -----------------------------------------------------------
def _solve(A, B):
    n = len(B)
    M = [row[:] + [B[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        if abs(M[p][c]) < 1e-12:
            raise ValueError("degenerate quad")
        M[c], M[p] = M[p], M[c]
        pv = M[c][c]
        M[c] = [v / pv for v in M[c]]
        for r in range(n):
            if r != c and M[r][c]:
                f = M[r][c]
                M[r] = [v - f * w for v, w in zip(M[r], M[c])]
    return [M[i][n] for i in range(n)]


def perspective_coeffs(dest, src):
    A, B = [], []
    for (dx, dy), (sx, sy) in zip(dest, src):
        A.append([dx, dy, 1, 0, 0, 0, -dx * sx, -dy * sx]); B.append(sx)
        A.append([0, 0, 0, dx, dy, 1, -dx * sy, -dy * sy]); B.append(sy)
    return _solve(A, B)


def warp_region(card, quad, pad=0):
    """Project a card onto just the bounding box of its quad rather than the
    whole canvas.  Much faster, which matters once there are hundreds of
    frames instead of fourteen."""
    xs = [p[0] for p in quad]
    ys = [p[1] for p in quad]
    x0 = int(math.floor(min(xs))) - pad
    y0 = int(math.floor(min(ys))) - pad
    x1 = int(math.ceil(max(xs))) + pad
    y1 = int(math.ceil(max(ys))) + pad
    w, h = max(1, x1 - x0), max(1, y1 - y0)
    local = [(x - x0, y - y0) for x, y in quad]
    cw, ch = card.size
    co = perspective_coeffs(local, [(0, 0), (cw, 0), (cw, ch), (0, ch)])
    out = card.transform((w, h), Image.PERSPECTIVE, co,
                         resample=Image.BICUBIC, fillcolor=(0, 0, 0, 0))
    return out, (x0, y0)


def paste_layer(dst, layer, pos):
    """alpha_composite that tolerates a layer hanging off the canvas edge."""
    x, y = pos
    cx0, cy0 = max(0, x), max(0, y)
    lx0, ly0 = cx0 - x, cy0 - y
    lx1 = min(layer.width, W - x)
    ly1 = min(layer.height, H - y)
    if lx1 <= lx0 or ly1 <= ly0:
        return
    dst.alpha_composite(layer.crop((lx0, ly0, lx1, ly1)), (cx0, cy0))


# ---- ink -------------------------------------------------------------------
def brush_stroke(width, thickness=10, seed=7, color=(240, 244, 250)):
    """A tapered stroke with dry-brush breaks.  Deterministic, so it does not
    flicker between frames."""
    h = thickness * 6
    layer = Image.new("RGBA", (width, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    rnd = random.Random(seed)
    gaps = [(rnd.uniform(0.18, 0.86), rnd.uniform(0.012, 0.045)) for _ in range(5)]

    steps = width * 3
    for i in range(steps):
        t = i / (steps - 1)
        taper = math.sin(math.pi * (t ** 0.72)) ** 0.5
        th = thickness * taper
        if th < 0.4:
            continue
        y = h / 2 + math.sin(t * 2.6 + 0.4) * thickness * 0.30
        a = 236 * taper
        for g, gw in gaps:
            if abs(t - g) < gw:
                a *= 0.10 + 0.9 * (abs(t - g) / gw)
        a *= 0.86 + rnd.random() * 0.14
        x = t * (width - 1)
        d.ellipse([x - th * 0.5, y - th, x + th * 0.5, y + th],
                  fill=color + (int(max(0, min(255, a))),))

    for _ in range(3):
        t0 = rnd.uniform(0.62, 0.80)
        y = h / 2 + rnd.uniform(-1, 1) * thickness * 0.55
        d.line([(t0 * width, y), (width - rnd.uniform(2, 26), y)],
               fill=color + (rnd.randint(40, 95),), width=1)
    return layer.filter(ImageFilter.GaussianBlur(0.6))


def draw_tracked(draw, xy, text, font, fill, tracking=0):
    """Pillow has no letter-spacing, so place each glyph by hand."""
    widths = [draw.textlength(c, font=font) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x, y = xy
    x -= total / 2
    for c, w in zip(text, widths):
        draw.text((x, y), c, font=font, fill=fill, anchor="lm")
        x += w + tracking


# ---- tracklist / lyrics ----------------------------------------------------
SAMPLE_TRACKS = """# start | korean | english | album no. | romanised
00:00 | 왕의 길목 | The King's Path | 1 | Wangui Gilmok
00:00 | END
"""
SAMPLE_LYRICS = """# track no. | korean | romanised | english
01 | 왕의 길목에 서서 | Wangui gilmoge seoseo | Standing at the king's crossing
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
        TRACKLIST.write_text(SAMPLE_TRACKS, encoding="utf-8")
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
                     int(p[3]) if len(p) > 3 and p[3].isdigit() else 1,
                     p[4] if len(p) > 4 else ""))

    tracks = []
    for i, (t, kr, en, al, rr) in enumerate(rows):
        if not kr or kr.upper() == "END":
            break
        if i + 1 >= len(rows):
            sys.exit("[ERROR] the last track has no end time - add a final END line")
        tracks.append({"n": i + 1, "start": t, "end": rows[i + 1][0],
                       "kr": kr, "en": en, "album": al, "rr": rr})
    if not tracks:
        sys.exit("[ERROR] no tracks found")
    return tracks


def read_lyrics(tracks):
    if not LYRICS.exists():
        LYRICS.write_text(SAMPLE_LYRICS, encoding="utf-8")
        print(f"[created] {LYRICS} - fill it in for the lyric lines")
    table = {}
    for ln in LYRICS.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        p = [x.strip() for x in ln.split("|")]
        if p[0].isdigit():
            table[int(p[0])] = (p[1] if len(p) > 1 else "",
                                p[2] if len(p) > 2 else "",
                                p[3] if len(p) > 3 else "")
    for t in tracks:
        t["lyric"] = table.get(t["n"], ("", "", ""))
    missing = [t["n"] for t in tracks if not t["lyric"][0]]
    if missing:
        print(f"[note] no lyric line for track(s): {missing}")
    return tracks


# ---- artwork ---------------------------------------------------------------
def make_background(palette="sea"):
    BG_CORE, BG_EDGE = BG_PALETTE.get(palette, BG_PALETTE["sea"])
    small = Image.new("RGB", (W // 8, H // 8))
    px = small.load()
    cx, cy = small.width / 2, small.height * 0.44
    maxd = math.hypot(cx, cy)
    for y in range(small.height):
        for x in range(small.width):
            dd = math.hypot((x - cx) * 0.82, y - cy) / maxd
            f = min(1.0, dd ** 1.25)
            px[x, y] = tuple(int(BG_CORE[i] + (BG_EDGE[i] - BG_CORE[i]) * f)
                             for i in range(3))
    bg = small.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(24))

    if BG_IMAGE.exists() and HERO_OPACITY > 0:
        art = Image.open(BG_IMAGE).convert("RGB")
        r = max(W / art.width, H / art.height)
        art = art.resize((int(art.width * r), int(art.height * r)), Image.LANCZOS)
        l = (art.width - W) // 2
        t = int((art.height - H) * 0.42)
        art = art.crop((l, t, l + W, t + H))
        if HERO_BLUR:
            art = art.filter(ImageFilter.GaussianBlur(HERO_BLUR))
        art = ImageEnhance.Color(art).enhance(HERO_SATURATION)

        m = Image.new("L", (W // 8, H // 8))
        mp = m.load()
        mcx, mcy = m.width / 2, m.height * 0.40
        mmax = math.hypot(mcx, mcy)
        for y in range(m.height):
            for x in range(m.width):
                dd = math.hypot((x - mcx) * 0.80, y - mcy) / mmax
                v = min(1.0, dd ** 0.9)
                v = v * HERO_CLEAR_CENTRE + (1 - HERO_CLEAR_CENTRE)
                mp[x, y] = int(255 * HERO_OPACITY * v)
        mask = m.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(30))
        bg = Image.composite(art, bg, mask)
    elif HERO_OPACITY > 0:
        print("[note] art/hero.jpg not found - plain backdrop")
    return bg


def rounded_mask(size, radius):
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size - 1, size - 1],
                                        radius=radius, fill=255)
    return m


def load_cover(track, size, seal, variant=0):
    candidates = [COVERS / f"{track['n']:02d}.{e}" for e in ("jpg", "jpeg", "png")]
    per_track = any(p.exists() for p in candidates)
    candidates += [COVERS / f"ch{track['album']}.{e}" for e in ("jpg", "jpeg", "png")]
    im = None
    for p in candidates:
        if p.exists():
            im = Image.open(p).convert("RGB")
            break
    if im is None:
        im = Image.new("RGB", (size, size), (46, 62, 80))

    zoom, ax, ay = COVER_VARIANTS[0] if per_track else \
        COVER_VARIANTS[variant % len(COVER_VARIANTS)]
    s = int(min(im.size) * zoom)
    x = int((im.width - s) * ax)
    y = int((im.height - s) * ay)
    im = im.crop((x, y, x + s, y + s))
    im = im.resize((size, size), Image.LANCZOS).convert("RGBA")

    if seal is not None:
        ss = int(size * 0.20)
        st = seal.resize((ss, ss), Image.LANCZOS)
        im.alpha_composite(st, (int(size * 0.045), int(size * 0.72)))

    im.putalpha(rounded_mask(size, int(size * 0.045)))
    return im


def make_tinted(card, tint):
    """The fully washed-out version of a card.  At render time the clean and
    washed versions are blended, so the wash comes on gradually as the card
    rotates away from the middle."""
    rgb = ImageEnhance.Color(card.convert("RGB")).enhance(0.55)
    rgb = Image.blend(rgb, Image.new("RGB", rgb.size, tint), 0.34)
    rgb = ImageEnhance.Brightness(rgb).enhance(0.86)
    out = rgb.convert("RGBA")
    out.putalpha(card.split()[-1])
    return out


# ---- the carousel ----------------------------------------------------------
CENTER_SIZE = 512
CY = 500
HALF = CENTER_SIZE // 2
VISIBLE = 2.9        # cards fade out past this many places from the middle


def slot_geometry(u):
    """Continuous form of the old five-slot table.  u is how many places the
    card sits from the middle and may be fractional, which is what makes the
    rotation possible."""
    a = abs(u)
    if a > VISIBLE:
        return None
    mid_x = 960 + (1 if u > 0 else -1) * 484 * (a ** 0.67) if u else 960
    scale = 1.0 / (1 + 0.24 * a ** 1.5)          # overall size
    fore = 1.0 / (1 + 0.52 * a ** 0.75)          # horizontal foreshortening
    skew = 1 + 0.215 * (min(a, VISIBLE) ** 0.4)  # near edge taller than far
    height = HALF * scale
    h_near = height * math.sqrt(skew)
    h_far = height / math.sqrt(skew)
    half_w = max(2.0, HALF * scale * fore)

    if a <= 2:
        alpha = 255 - 32 * (a ** 1.1)
    else:
        alpha = 190 * max(0.0, (VISIBLE - a) / (VISIBLE - 2))
    return mid_x, h_far, h_near, half_w, max(0.0, alpha)


def card_quad(u, mid_x, h_far, h_near, half_w):
    xl, xr = mid_x - half_w, mid_x + half_w
    if u < 0:                       # left of centre: the right edge is nearer
        hl, hr = h_far, h_near
    elif u > 0:
        hl, hr = h_near, h_far
    else:
        hl = hr = h_far
    return [(xl, CY - hl), (xr, CY - hr), (xr, CY + hr), (xl, CY + hl)]


def draw_carousel(base, tracks, pos, covers, tints):
    n = len(tracks)
    order = []
    for k in range(int(math.floor(pos - VISIBLE)), int(math.ceil(pos + VISIBLE)) + 1):
        u = k - pos
        g = slot_geometry(u)
        if g:
            order.append((abs(u), u, tracks[k % n], g))
    order.sort(key=lambda o: -o[0])          # far cards first, centre last

    for a, u, t, (mid_x, h_far, h_near, half_w, alpha) in order:
        card = covers[t["n"]]
        wash = min(1.0, a)
        if wash > 0.01:
            card = Image.blend(card, tints[t["n"]], wash)

        quad = card_quad(u, mid_x, h_far, h_near, half_w)

        sil = Image.new("RGBA", card.size, (0, 0, 0, 255))
        sil.putalpha(card.split()[-1])
        blur = 26 if a < 0.5 else 14
        sh, off = warp_region(sil, [(x, y + 16) for x, y in quad], pad=blur * 2)
        sh = sh.filter(ImageFilter.GaussianBlur(blur))
        k = (0.60 if a < 0.5 else 0.28) * (alpha / 255)
        sh.putalpha(sh.split()[-1].point(lambda v: int(v * k)))
        paste_layer(base, sh, off)

        proj, off = warp_region(card, quad)
        if alpha < 254:
            proj.putalpha(proj.split()[-1].point(lambda v: int(v * alpha / 255)))
        paste_layer(base, proj, off)


# ---- the player bar --------------------------------------------------------
BAR = (320, 932, 1600, 1032)


def draw_bar_pill(img):
    pill = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x0, y0, x1, y1 = BAR
    ImageDraw.Draw(pill).rounded_rectangle([x0, y0, x1, y1],
                                           radius=(y1 - y0) // 2,
                                           fill=BAR_FILL + (238,))
    img.alpha_composite(pill)


def draw_bar_contents(layer, tracks, t, covers, fonts):
    f_bar_kr, f_bar_sub = fonts
    d = ImageDraw.Draw(layer)
    cy = (BAR[1] + BAR[3]) // 2
    ic = BRIGHT

    def bar(x, w=4, h=22):
        d.rectangle([x, cy - h // 2, x + w, cy + h // 2], fill=ic)

    d.polygon([(392, cy), (412, cy - 13), (412, cy + 13)], fill=ic); bar(386)
    bar(430, 5, 26); bar(444, 5, 26)
    d.polygon([(508, cy), (488, cy - 13), (488, cy + 13)], fill=ic); bar(510)

    layer.alpha_composite(covers[t["n"]].resize((68, 68), Image.LANCZOS),
                          (556, cy - 34))

    d.text((648, cy - 14), t["kr"], font=f_bar_kr, fill=BRIGHT, anchor="lm")
    album_en = ALBUM_NAMES.get(t["album"], ("", ""))[1].upper()
    sub = f"{album_en}   ·   {t['rr']} : {t['en'].upper()}" if t["rr"] \
        else f"{album_en}   ·   {t['en'].upper()}"
    d.text((648, cy + 14), sub, font=f_bar_sub, fill=(150, 150, 155), anchor="lm")

    rnd = random.Random(t["n"] * 977)
    wx0, wx1 = 1330, 1568
    bars = (wx1 - wx0) // 3
    played = int(bars * (t["n"] - 0.5) / len(tracks))
    for i in range(bars):
        hgt = int(4 + abs(math.sin(i * 0.7)) * 10 + rnd.random() * 16)
        x = wx0 + i * 3
        col = (216, 210, 204) if i <= played else (104, 100, 98)
        d.rectangle([x, cy - hgt // 2, x + 1, cy + hgt // 2], fill=col)


# ---- frame -----------------------------------------------------------------
def render(tracks, pos, backdrops, fonts, covers, tints, text_mode=None):
    (f_title, f_big, f_ly_kr, f_ly_rr, f_ly_en, f_sub, f_bar_kr, f_bar_sub) = fonts
    text_mode = text_mode or TEXT_MODE
    n = len(tracks)

    i0 = int(math.floor(pos + 1e-9))
    frac = pos - i0
    t_out = tracks[i0 % n]
    t_in = tracks[(i0 + 1) % n]
    t_now = t_out if frac < 0.5 else t_in

    # the backdrop cross fades when a transition crosses into another trilogy
    k_out = trilogy_of(t_out["album"])[0]
    k_in = trilogy_of(t_in["album"])[0]
    if frac < 1e-6 or k_out == k_in:
        bg = backdrops[k_out if frac < 0.5 else k_in]
    else:
        f = frac * frac * (3 - 2 * frac)
        bg = Image.blend(backdrops[k_out], backdrops[k_in], f)

    img = bg.copy().convert("RGBA")
    d = ImageDraw.Draw(img)

    # the header does not change between tracks, so it never fades
    if COMP_TITLE_KR or COMP_TITLE_EN:
        d.text((W // 2, 62), COMP_TITLE_KR or COMP_TITLE_EN,
               font=f_title, fill=BRIGHT, anchor="mm")
        draw_tracked(d, (W // 2, 114), COMP_TITLE_EN, f_big, BRIGHT, tracking=11)
        if BRUSH_WIDTH:
            st = brush_stroke(BRUSH_WIDTH)
            img.alpha_composite(st, ((W - st.width) // 2, 122))
        if COMP_TAGLINE:
            d.text((W // 2, 198), COMP_TAGLINE, font=f_sub,
                   fill=(178, 194, 210), anchor="mm")

    draw_carousel(img, tracks, pos, covers, tints)
    draw_bar_pill(img)

    # everything that names the current track sits on its own layer, so it can
    # drop out and come back while the cards are moving
    if text_mode == "fade" and frac > 1e-6:
        a = max(0.0, 1 - 2.5 * min(frac, 1 - frac))
    else:
        a = 1.0

    if a > 0.004:
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        tri = trilogy_of(t_now["album"])[1]
        ld.text((1856, 66), f"{t_now['n']:02d} / {n:02d}",
                font=f_sub, fill=tri["accent"], anchor="rm")
        ld.text((1856, 94), tri["en"], font=f_sub, fill=tri["accent"], anchor="rm")

        kr, rr, en = t_now["lyric"]
        if kr:
            ld.text((W // 2, 790), kr, font=f_ly_kr, fill=BRIGHT, anchor="mm")
        if rr:
            ld.text((W // 2, 838), f"({rr})", font=f_ly_rr, fill=DIM, anchor="mm")
        if en:
            ld.text((W // 2, 882), en, font=f_ly_en,
                    fill=(232, 238, 246), anchor="mm")

        draw_bar_contents(layer, tracks, t_now, covers, (f_bar_kr, f_bar_sub))

        if a < 0.999:
            layer.putalpha(layer.split()[-1].point(lambda v: int(v * a)))
        img.alpha_composite(layer)

    return img.convert("RGB")


# ---- youtube thumbnail -----------------------------------------------------
def render_thumbnail(seal):
    """1280x720.  Built to survive being shrunk to a 320px strip: one picture,
    two words of English at a size you can read from across the room."""
    TW, TH = 1280, 720

    # a warm-to-cold wash across the frame, the three trilogies in one image
    small = Image.new("RGB", (TW // 8, TH // 8))
    px = small.load()
    keys = ["fire", "sea", "iron"]
    for x in range(small.width):
        t = x / (small.width - 1) * (len(keys) - 1)
        i = min(int(t), len(keys) - 2)
        f = t - i
        a_core, a_edge = BG_PALETTE[keys[i]]
        b_core, b_edge = BG_PALETTE[keys[i + 1]]
        core = [a_core[c] + (b_core[c] - a_core[c]) * f for c in range(3)]
        edge = [a_edge[c] + (b_edge[c] - a_edge[c]) * f for c in range(3)]
        for y in range(small.height):
            v = abs(y / (small.height - 1) - 0.42) * 1.9
            px[x, y] = tuple(int(core[c] + (edge[c] - core[c]) * min(1, v ** 1.2))
                             for c in range(3))
    img = small.resize((TW, TH), Image.BICUBIC) \
               .filter(ImageFilter.GaussianBlur(18)).convert("RGBA")

    # the picture on the right, dissolving into the background on its left edge
    src = THUMB_IMAGE
    if not src.exists():
        for e in ("jpg", "jpeg", "png"):
            if (COVERS / f"ch1.{e}").exists():
                src = COVERS / f"ch1.{e}"
                break
    if src.exists():
        pic = Image.open(src).convert("RGB")
        sq = min(pic.size)
        pic = pic.crop(((pic.width - sq) // 2, (pic.height - sq) // 2,
                        (pic.width + sq) // 2, (pic.height + sq) // 2))
        pic = pic.resize((TH + 60, TH + 60), Image.LANCZOS).convert("RGBA")
        fade = Image.new("L", pic.size, 255)
        fd = ImageDraw.Draw(fade)
        for i in range(300):
            fd.line([(i, 0), (i, pic.height)], fill=int(255 * (i / 300) ** 0.8))
        pic.putalpha(fade)
        img.alpha_composite(pic, (TW - pic.width + 90, -30))
    else:
        print("[note] no art/thumb.jpg and no covers/ch1 - picture panel skipped")

    d = ImageDraw.Draw(img)
    f_kr = load_font(50, "bold")
    f_en = load_font(96, "bold")
    f_sm = load_font(25, "bold")

    d.text((66, 236), COMP_TITLE_KR, font=f_kr, fill=BRIGHT, anchor="lm")

    # two lines, not one word per line - "OF" alone on a row wastes the space
    words = COMP_TITLE_EN.split()
    rows = [" ".join(words[:-1]), words[-1]] if len(words) > 1 else words
    rows = [r for r in rows if r]
    y = 322
    for r in rows:
        while f_en.size > 40 and d.textlength(r, font=f_en) > 560:
            f_en = load_font(f_en.size - 4, "bold")
        d.text((60, y), r, font=f_en, fill=BRIGHT, anchor="lm")
        y += int(f_en.size * 0.98)

    if BRUSH_WIDTH:
        st = brush_stroke(470, thickness=9)
        img.alpha_composite(st, (58, y - 46))
    if THUMB_LINE:
        d.text((66, y + 22), THUMB_LINE, font=f_sm,
               fill=(206, 218, 230), anchor="lm")

    if seal is not None:
        sz = 104
        img.alpha_composite(seal.resize((sz, sz), Image.LANCZOS), (62, 66))
    return img.convert("RGB")


# ---- main ------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", type=int)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--thumb", action="store_true",
                    help="render thumbnail.png (1280x720) and nothing else")
    ap.add_argument("--transitions", action="store_true")
    ap.add_argument("--fps", type=int, default=FPS)
    ap.add_argument("--dur", type=float, default=TRANSITION_SECONDS)
    ap.add_argument("--text", choices=["fade", "cut"], default=TEXT_MODE)
    ap.add_argument("--ease", choices=["ease", "smooth", "linear"], default=EASING)
    args = ap.parse_args()

    tracks = read_lyrics(read_tracklist())
    print(f"\n{len(tracks)} tracks\n")
    for t in tracks:
        print(f"  {t['n']:02d}  album {t['album']}  "
              f"{trilogy_of(t['album'])[0]:<4}  {t['kr']}")
    if args.check:
        return

    seal = None
    if MARK.exists():
        seal = Image.open(MARK).convert("RGBA")
        seal.putalpha(seal.split()[-1].point(lambda v: int(v * 0.92)))
    else:
        print("[note] art/mark.png not found - cards will carry no seal")

    if not args.thumb:
        used = sorted({trilogy_of(t["album"])[0] for t in tracks})
        print(f"\nbuilding {len(used)} backdrop(s): {', '.join(used)}...")
        backdrops = {k: make_background(k) for k in used}

    if args.thumb:
        out = BASE / "thumbnail.png"
        render_thumbnail(seal).save(out)
        print(f"\n{out}")
        return

    seen, covers = {}, {}
    for t in tracks:
        v = seen.get(t["album"], 0)
        seen[t["album"]] = v + 1
        covers[t["n"]] = load_cover(t, CENTER_SIZE, seal, v)
    if max(seen.values()) > 1:
        print("[note] albums reused across tracks - repeats get a different crop")
    tints = {t["n"]: make_tinted(covers[t["n"]], SIDE_TINTS[t["n"] % len(SIDE_TINTS)])
             for t in tracks}

    fonts = (load_font(38, "bold"), load_font(34, "bold"),
             load_font(38), load_font(27, "italic"), load_font(29),
             load_font(16), load_font(25, "bold"), load_font(15))

    FRAMES.mkdir(exist_ok=True)
    print()
    for t in tracks:
        if args.preview and t["n"] != args.preview:
            continue
        render(tracks, t["n"] - 1, backdrops, fonts, covers, tints,
               args.text).save(FRAMES / f"track_{t['n']:02d}.png")
        print(f"  rendered track_{t['n']:02d}.png")

    if args.preview:
        print(f"\nopen {FRAMES}")
        return

    if not args.transitions:
        print(f"\n{len(tracks)} stills in {FRAMES}")
        print("run again with --transitions for the rotations between them")
        return

    steps = max(2, int(round(args.dur * args.fps)))
    TRANS.mkdir(exist_ok=True)
    have_ffmpeg = bool(shutil.which("ffmpeg"))
    print(f"\n{len(tracks)} transitions x {steps - 1} frames "
          f"({args.dur}s at {args.fps}fps)\n")

    for i in range(len(tracks)):
        a = tracks[i]["n"]
        b = tracks[(i + 1) % len(tracks)]["n"]
        out = TRANS / f"{a:02d}_to_{b:02d}"
        out.mkdir(exist_ok=True)
        for j in range(1, steps):
            pos = i + ease(j / steps, args.ease)
            render(tracks, pos, backdrops, fonts, covers, tints,
                   args.text).save(out / f"f{j:04d}.png")
        print(f"  {out.name}  ({steps - 1} frames)", end="")
        if have_ffmpeg:
            subprocess.run(
                ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(args.fps),
                 "-start_number", "1", "-i", str(out / "f%04d.png"),
                 "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                 "-pix_fmt", "yuv420p", str(TRANS / f"{a:02d}_to_{b:02d}.mp4")],
                check=False)
            print("  -> mp4", end="")
        print()

    print(f"\nstills in {FRAMES}\ntransitions in {TRANS}")
    if not have_ffmpeg:
        print("ffmpeg not on PATH - the mp4s were skipped, "
              "import the numbered folders as image sequences instead")


if __name__ == "__main__":
    main()
