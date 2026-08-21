#!/usr/bin/env python3
"""Redraw the classic X11 core cursors at hidpi sizes.

The cursor font is bitmap-locked at ~16px; Adwaita is the wrong kind of
modern. This redraws the classic shapes as 16x16 pixel art, adds the
white halo the cursor-font masks used to provide, scales by integer
factors (nearest neighbour -- crisp corners, no antialiasing, that IS
the aesthetic), and writes Xcursor files directly; no xcursorgen needed.

Install:  ./cursors.py [themedir]
          default themedir ~/.local/share/icons/tyler-classic
Preview:  ./cursors.py --preview out.pam   (16px art, one row per shape)
"""
import os, struct, sys

SIZES = (16, 32, 48, 64)

def grid(*rows):
    assert all(len(r) == 16 for r in rows) and len(rows) == 16
    return [list(r) for r in rows]

def blank():
    return [["."] * 16 for _ in range(16)]

# ---------------------------------------------------------------- art

# The pointer. Solid head, split tail, hot at the tip.
LEFT_PTR = grid(
    ".#..............",
    ".##.............",
    ".###............",
    ".####...........",
    ".#####..........",
    ".######.........",
    ".#######........",
    ".########.......",
    ".#########......",
    ".##########.....",
    ".######.........",
    ".###.###........",
    ".##..###........",
    ".#....###.......",
    "......###.......",
    ".......##.......",
)

# The move cursor: four-way arrows.
FLEUR = grid(
    ".......##.......",
    "......####......",
    ".....######.....",
    ".......##.......",
    ".......##.......",
    "..#....##....#..",
    ".##....##....##.",
    "################",
    "################",
    ".##....##....##.",
    "..#....##....#..",
    ".......##.......",
    ".......##.......",
    ".....######.....",
    "......####......",
    ".......##.......",
)

# The resize cursor: NW and SE solid heads joined by a 2px diagonal.
def sizing():
    g = blank()
    for r in range(6):
        for c in range(6 - r):
            g[r][c] = "#"
            g[15 - r][15 - c] = "#"
    for i in range(3, 13):
        g[i][i] = g[i][min(i + 1, 15)] = "#"
    return g

# The I-beam, hot in the middle of the stem.
def xterm():
    g = blank()
    for c in range(5, 11):
        g[1][c] = g[14][c] = "#"
    for r in range(2, 14):
        g[r][7] = g[r][8] = "#"
    return g

# The pointing hand browsers want for links (CSS cursor: pointer).
# The core font has hand2, but the CSS name "pointer" has no font
# fallback, so links get the arrow unless a theme provides this.
HAND2 = grid(
    "......##........",
    "......##........",
    "......##........",
    "......##........",
    "......##........",
    "......####......",
    "......######....",
    "......########..",
    "..##..########..",
    "..############..",
    "...###########..",
    "...###########..",
    "....##########..",
    "....##########..",
    ".....########...",
    ".....########...",
)

# name -> (art, xhot, yhot) at the 16px base
SHAPES = {
    "left_ptr":       (LEFT_PTR, 1, 0),
    "top_left_arrow": (LEFT_PTR, 1, 0),
    "sizing":         (sizing(), 8, 8),
    "fleur":          (FLEUR, 8, 8),
    "xterm":          (xterm(), 8, 8),
}

ALIASES = {
    "arrow": "left_ptr", "default": "left_ptr",
    "text": "xterm", "ibeam": "xterm",
    "bd_double_arrow": "sizing", "nwse-resize": "sizing",
    "move": "fleur", "all-scroll": "fleur",
}

# ------------------------------------------------------------- render

def halo(art):
    """The cursor-font masks drew a white border around every shape;
    dilate by one so the cursor survives dark backgrounds."""
    out = [row[:] for row in art]
    for r in range(16):
        for c in range(16):
            if art[r][c] != "#":
                near = any(
                    0 <= r + dr < 16 and 0 <= c + dc < 16
                    and art[r + dr][c + dc] == "#"
                    for dr in (-1, 0, 1) for dc in (-1, 0, 1))
                if near:
                    out[r][c] = "o"
    return out

BLACK, WHITE, CLEAR = 0xFF000000, 0xFFFFFFFF, 0x00000000

def argb(art, scale):
    px = []
    for row in art:
        line = []
        for ch in row:
            v = BLACK if ch == "#" else WHITE if ch == "o" else CLEAR
            line.extend([v] * scale)
        for _ in range(scale):
            px.extend(line)
    return px

def xcursor(images):
    """images: list of (nominal, width, height, xhot, yhot, pixels)."""
    ntoc = len(images)
    toc_end = 16 + 12 * ntoc
    chunks, toc, pos = [], [], toc_end
    for nominal, w, h, xh, yh, px in images:
        chunk = struct.pack("<9I", 36, 0xFFFD0002, nominal, 1,
                            w, h, xh, yh, 0)
        chunk += struct.pack("<%dI" % len(px), *px)
        toc.append(struct.pack("<3I", 0xFFFD0002, nominal, pos))
        chunks.append(chunk)
        pos += len(chunk)
    return (b"Xcur" + struct.pack("<3I", 16, 0x10000, ntoc)
            + b"".join(toc) + b"".join(chunks))

# The finger-only theme: just the link hand, at core-font scale (16px),
# so it sits beside the untouched 1987 arrows without towering over
# them. Every name not present falls back to the core cursor font.
FINGER_SHAPES = {"hand2": (HAND2, 7, 0)}
FINGER_ALIASES = {"pointer": "hand2", "pointing_hand": "hand2",
                  "hand": "hand2", "hand1": "hand2"}

def write_theme(themedir, name="tyler-classic", shapes=SHAPES,
                aliases=ALIASES, sizes=SIZES):
    cur = os.path.join(themedir, "cursors")
    os.makedirs(cur, exist_ok=True)
    with open(os.path.join(themedir, "index.theme"), "w") as f:
        f.write("[Icon Theme]\nName=%s\n"
                "Comment=The cursors of old, redrawn\n" % name)
    for shape, (art, xh, yh) in shapes.items():
        haloed = halo(art)
        images = [(s, s, s, xh * (s // 16), yh * (s // 16),
                   argb(haloed, s // 16)) for s in sizes]
        with open(os.path.join(cur, shape), "wb") as f:
            f.write(xcursor(images))
    for alias, target in aliases.items():
        path = os.path.join(cur, alias)
        if not os.path.lexists(path):
            os.symlink(target, path)
    print("theme written to", themedir)

def write_preview(path):
    """One row per shape at 48px, PAM RGBA."""
    shapes = list(SHAPES.items())
    w, h = 48 * len(shapes), 48
    rows = [[(64, 64, 64, 255)] * w for _ in range(h)]
    for i, (name, (art, _, _)) in enumerate(shapes):
        px = argb(halo(art), 3)
        for r in range(48):
            for c in range(48):
                v = px[r * 48 + c]
                if v:
                    rows[r][i * 48 + c] = (
                        (v >> 16) & 255, (v >> 8) & 255, v & 255, 255)
    with open(path, "wb") as f:
        f.write(b"P7\nWIDTH %d\nHEIGHT %d\nDEPTH 4\nMAXVAL 255\n"
                b"TUPLTYPE RGB_ALPHA\nENDHDR\n" % (w, h))
        for row in rows:
            f.write(bytes(b for p in row for b in p))
    print("preview written to", path)

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--preview":
        write_preview(sys.argv[2])
    elif len(sys.argv) > 1 and sys.argv[1] == "--finger":
        write_theme(sys.argv[2] if len(sys.argv) > 2 else
                    os.path.expanduser("~/.local/share/icons/tyler-finger"),
                    name="tyler-finger", shapes=FINGER_SHAPES,
                    aliases=FINGER_ALIASES, sizes=(16,))
    else:
        write_theme(sys.argv[1] if len(sys.argv) > 1 else
                    os.path.expanduser("~/.local/share/icons/tyler-classic"))
