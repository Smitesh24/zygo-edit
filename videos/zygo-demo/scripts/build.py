"""Generate compositions/demo.html (split-screen live demo) and index.html (master timeline + mix)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VO_DUR = json.loads((ROOT / "assets/vo/durations.json").read_text())

# ------------------------------------------------------------------ master grid (100 BPM, bar = 2.4s)
SCENES = [  # id, start, duration — app demo first (hook + full demo), then the explanation
    ("hook", 0.0, 12.0),
    ("demo", 12.0, 64.8),
    ("problem", 76.8, 16.8),
    ("solution", 93.6, 14.4),
    ("impact", 108.0, 16.8),
    ("traction", 124.8, 21.6),
    ("outro", 146.4, 9.6),
]
TOTAL = 156.0
DEMO0 = 12.0

VO = [  # id, absolute start
    ("hook-1", 0.5), ("hook-2", 4.2), ("hook-3", 8.6),
    ("demo-intro", DEMO0 + 0.3), ("demo-scan", DEMO0 + 7.8), ("demo-quote", DEMO0 + 14.2),
    ("demo-escrow", DEMO0 + 21.6), ("demo-accept", DEMO0 + 29.8), ("demo-payout", DEMO0 + 35.3),
    ("demo-confirm", DEMO0 + 44.4), ("demo-settle", DEMO0 + 52.9),
    ("problem-1", 77.1), ("problem-2", 81.3),
    ("solution-1", 93.9), ("solution-2", 97.4),
    ("impact-1", 108.3), ("impact-2", 111.1),
    ("traction-1", 125.2), ("traction-2", 139.0),
    ("outro", 147.0),
]

# ------------------------------------------------------------------ demo edit decision list
# (T0, T1, source start, playback rate) in demo-local seconds. Source = assets/footage/{user,lp}.mp4,
# which share the screen recording's clock. Dead time (file pickers, Mission Control, idle waits) is cut.
USER = [
    (0.0, 7.6, 0.6, 0.45),     # home, idle
    (7.6, 8.35, 3.7, 1.0),     # cursor to Upload QR
    (8.35, 9.9, 9.45, 1.0),    # QR decoded -> paying GLOCAL Arena Cafe
    (9.9, 11.7, 11.6, 1.0),    # types 10
    (11.7, 14.0, 14.4, 1.0),   # Get quote
    (14.0, 19.6, 17.35, 0.3),  # Review & pay (slowed, zoomed)
    (19.6, 21.4, 19.03, 0.7),  # Confirm & pay -> opening wallet
    (21.4, 24.4, 24.15, 0.2),  # (under wallet overlay) ready to fund
    (24.4, 25.2, 24.75, 1.0),  # ready to fund
    (25.2, 26.0, 48.5, 1.0),   # confirming deposit
    (26.0, 29.6, 60.2, 1.0),   # escrow funded -> offer out
    (29.6, 31.2, 63.8, 1.0),
    (31.2, 33.6, 66.9, 1.0),   # provider assigned
    (33.6, 35.0, 69.3, 1.0),
    (35.0, 38.8, 70.7, 1.0),
    (38.8, 40.2, 74.5, 1.0),
    (40.2, 43.1, 84.55, 1.0),  # order marked paid by provider
    (43.1, 44.2, 87.45, 1.0),
    (44.2, 45.7, 88.55, 1.0),
    (45.7, 47.6, 92.45, 1.0),  # I confirm merchant was paid
    (47.6, 49.65, 94.35, 0.15),  # (under wallet overlay)
    (49.65, 52.0, 97.3, 1.0),  # payment confirmed
    (52.0, 52.6, 99.65, 1.0),  # Done
    (52.6, 55.2, 108.9, 1.0),  # payment successful, settled on-chain
    (55.2, 58.6, 111.5, 1.0),
    (58.6, 62.4, 114.9, 0.35), # timeline: settling -> completed
    (62.4, 64.8, 117.6, 1.0),  # history: completed
]
LP = [
    (0.0, 21.4, 44.2, 0.2),    # LP desk online, waiting
    (21.4, 26.0, 48.48, 0.15),
    (26.0, 29.6, 50.45, 1.0),  # new payment request
    (29.6, 31.2, 54.05, 1.0),
    (31.2, 33.6, 66.9, 1.0),   # Accept
    (33.6, 35.0, 69.3, 1.0),
    (35.0, 38.8, 70.7, 1.0),   # merchant UPI QR
    (38.8, 40.2, 74.5, 1.0),   # Mark Paid
    (40.2, 43.1, 84.55, 1.0),  # receipt saved -> Submit
    (43.1, 44.2, 87.45, 1.0),
    (44.2, 45.7, 88.55, 1.0),
    (45.7, 47.6, 92.45, 1.0),
    (47.6, 49.65, 94.35, 0.15),
    (49.65, 52.6, 97.3, 1.0),  # settlement in progress
    (52.6, 55.2, 108.9, 1.0),
    (55.2, 56.0, 47.0, 1.0),   # before: USDC received 64.7
    (56.0, 58.6, 111.4, 1.0),  # after: 64.8
    (58.6, 64.8, 123.2, 1.0),  # history: received 0.10 USDC
]
WALLET = [  # file, T0, T1, proxy start, rate
    ("wallet-approve", 21.2, 24.6, 1.09, 0.55),
    ("wallet-sign", 47.4, 49.65, 0.92, 0.6),
]
# camera keyframes: (T, panel, scale, x, y, dur) — x/y in 960x1670 source-crop px
CAM = [
    (10.5, "u", 1.55, 480, 640, 0.7),
    (12.6, "u", 1.0, 480, 835, 0.6),
    (14.25, "u", 1.15, 470, 560, 0.8),
    (19.45, "u", 1.0, 480, 835, 0.5),
    (25.0, "u", 1.2, 480, 1250, 0.8),
    (29.3, "u", 1.0, 480, 835, 0.6),
    (29.7, "l", 1.15, 480, 1330, 0.8),
    (33.5, "l", 1.0, 480, 835, 0.5),
    (35.2, "l", 1.5, 480, 1200, 0.8),
    (38.7, "l", 1.2, 480, 1350, 0.6),
    (43.0, "l", 1.2, 480, 1390, 0.5),
    (44.3, "l", 1.0, 480, 835, 0.6),
    (44.0, "u", 1.25, 480, 900, 0.7),
    (47.2, "u", 1.0, 480, 835, 0.4),
    (49.75, "u", 1.2, 480, 900, 0.7),
    (52.5, "u", 1.2, 480, 950, 0.5),
    (55.0, "u", 1.0, 480, 835, 0.6),
    (55.2, "l", 1.6, 560, 1240, 0.7),
    (58.5, "l", 1.25, 480, 540, 0.8),
    (58.6, "u", 1.2, 480, 1000, 0.8),
    (62.3, "u", 1.0, 480, 835, 0.8),
    (62.3, "l", 1.0, 480, 835, 0.8),
]
FOCUS = [(0.0, "both"), (7.6, "u"), (29.4, "l"), (44.2, "u"), (55.2, "l"), (58.6, "both")]
STEPS = [(7.6, 1), (14.0, 2), (21.4, 3), (35.0, 4), (44.2, 5), (62.4, 6)]
STATES = [
    (0.0, "scanning"), (14.0, "quoted"), (19.65, "awaiting_escrow"), (24.4, "escrow_pending"),
    (26.0, "escrow_funded"), (27.3, "offer_pending"), (33.3, "lp_assigned"), (38.9, "fiat_processing"),
    (42.6, "fiat_sent"), (49.7, "user_confirmed"), (52.6, "settling"), (55.6, "completed"),
]
CALLOUTS = [  # id, T0, T1, left, top, text, accent
    ("c6", 59.1, 62.2, 860, 330, "You received 0.10 USDC \u00b7 Completed", "ink"),
]

PANEL_W, PANEL_H = 517, 900
SRC_W, SRC_H = 960, 1670
K = PANEL_W / SRC_W
PANELS = {"u": (680, 150), "l": (1267, 150)}


def r3(x):
    return f"{x:.3f}".rstrip("0").rstrip(".")


def video_tags(prefix, src, edl, extra_cls=""):
    out = []
    for i, (t0, t1, s0, rate) in enumerate(edl):
        rate_attr = f' data-playback-rate="{r3(rate)}"' if abs(rate - 1) > 1e-6 else ""
        out.append(
            f'<video id="{prefix}-{i}" class="dm-vid{extra_cls}" src="{src}" data-start="{r3(t0)}" '
            f'data-duration="{r3(t1 - t0)}" data-media-start="{r3(s0)}"{rate_attr} '
            f'data-track-index="{2 if prefix.startswith("dm-u") else 3}" data-hf-media-start-basis="local" muted playsinline></video>'
        )
    return "\n          ".join(out)


def cam_pose(scale, x, y):
    """translate so source point (x,y) sits at panel centre, clamped to keep the frame covered."""
    px, py = x * K, y * K
    tx = PANEL_W / 2 - scale * px
    ty = PANEL_H / 2 - scale * py
    tx = min(0, max(PANEL_W - scale * PANEL_W, tx))
    ty = min(0, max(PANEL_H - scale * PANEL_H, ty))
    return tx, ty


def build_demo():
    vids_u = video_tags("dm-u", "assets/footage/user.mp4", USER)
    vids_l = video_tags("dm-l", "assets/footage/lp.mp4", LP)
    wallet_vids = []
    for i, (f, t0, t1, s0, rate) in enumerate(WALLET):
        wallet_vids.append(
            f'<video id="dm-w-{i}" class="dm-wvid" src="assets/footage/{f}.mp4" data-start="{r3(t0)}" '
            f'data-duration="{r3(t1 - t0)}" data-media-start="{r3(s0)}" data-playback-rate="{r3(rate)}" '
            f'data-track-index="4" data-hf-media-start-basis="local" muted playsinline></video>'
        )
    wallet_vids = "\n          ".join(wallet_vids)

    js = []
    # camera
    for t, p, s, x, y, d in sorted(CAM):
        tx, ty = cam_pose(s, x, y)
        js.append(f'tl.to("#dm-{p}cam", {{ x: {tx:.1f}, y: {ty:.1f}, scale: {s}, duration: {d}, ease: "power3.inOut" }}, {t});')
    # focus dimming
    prev = None
    for t, f in FOCUS:
        u_dim = 0.5 if f == "l" else 0.0
        l_dim = 0.5 if f == "u" else 0.0
        js.append(f'tl.to("#dm-udim", {{ opacity: {u_dim}, duration: 0.5, ease: "power2.inOut" }}, {t});')
        js.append(f'tl.to("#dm-ldim", {{ opacity: {l_dim}, duration: 0.5, ease: "power2.inOut" }}, {t});')
        js.append(f'tl.to("#dm-uchip", {{ scale: {1.06 if f == "u" else 1}, duration: 0.4, ease: "back.out(2)" }}, {t});')
        js.append(f'tl.to("#dm-lchip", {{ scale: {1.06 if f == "l" else 1}, duration: 0.4, ease: "back.out(2)" }}, {t});')
    # steps: highlight box moves to the active row; finished rows get a check
    ROW_H = 98
    for t, n in STEPS:
        if n <= 5:
            js.append(f'tl.to("#dm-stephi", {{ y: {(n - 1) * ROW_H}, opacity: 1, duration: 0.5, ease: "power3.inOut" }}, {t});')
            js.append(f'tl.to("#dm-row{n}", {{ opacity: 1, duration: 0.3 }}, {t});')
        else:
            js.append(f'tl.to("#dm-stephi", {{ opacity: 0, duration: 0.4 }}, {t});')
        if n > 1:
            js.append(f'tl.fromTo("#dm-chk{n - 1}", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2.4)", immediateRender: false }}, {t - 0.1});')
    # order state roll
    for i, (t, _s) in enumerate(STATES):
        if i == 0:
            continue
        js.append(f'tl.to("#dm-states", {{ y: {-i * 36}, duration: 0.45, ease: "power3.inOut" }}, {t});')
    # callouts
    for cid, t0, t1, *_ in CALLOUTS:
        js.append(f'tl.fromTo("#dm-{cid}", {{ opacity: 0, x: -24, scale: 0.92 }}, {{ opacity: 1, x: 0, scale: 1, duration: 0.45, ease: "back.out(1.8)", immediateRender: false }}, {t0});')
        js.append(f'tl.to("#dm-{cid}", {{ opacity: 0, x: 16, duration: 0.3, ease: "power2.in" }}, {t1});')

    states_html = "".join(f'<span class="dm-state">{s}</span>' for _t, s in STATES)
    callouts_html = "\n        ".join(
        f'<div class="dm-callout dm-{acc}" id="dm-{cid}" style="left:{l}px;top:{tp}px"><span class="dm-dot"></span>{txt}</div>'
        for cid, _a, _b, l, tp, txt, acc in CALLOUTS
    )
    steps = [
        "Customer scans the merchant's existing QR code.",
        "Zygo shows the local amount and the total USDC cost.",
        "USDC moves into escrow; a matched provider is reserved.",
        "The provider pays the merchant in local currency.",
        "Payout is verified; escrow releases the USDC.",
    ]
    rows_html = "\n            ".join(
        f'<div class="dm-row" id="dm-row{i + 1}"><span class="dm-rlab">STEP {i + 1}</span><span class="dm-rtxt">{s}</span>'
        f'<svg class="dm-chk" id="dm-chk{i + 1}" viewBox="0 0 32 32"><circle cx="16" cy="16" r="15" fill="#0a5cf5"/>'
        f'<path d="M9 16.5l4.5 4.5L23 11.5" fill="none" stroke="#fff" stroke-width="3.2"/></svg></div>'
        for i, s in enumerate(steps)
    )
    ux, uy = PANELS["u"]
    lx, ly = PANELS["l"]
    # wallet overlay reveal: from the customer panel rect to full frame
    clip_from = f"inset({uy}px {1920 - ux - PANEL_W}px {1080 - uy - PANEL_H}px {ux}px round 26px)"
    clip_to = "inset(0px 0px 0px 0px round 0px)"

    html = (ROOT / "scripts/demo_template.html").read_text()
    html = (
        html.replace("{{VIDS_U}}", vids_u)
        .replace("{{VIDS_L}}", vids_l)
        .replace("{{WALLET_VIDS}}", wallet_vids)
        .replace("{{ROWS}}", rows_html)
        .replace("{{STATES}}", states_html)
        .replace("{{CALLOUTS}}", callouts_html)
        .replace("{{GEN_JS}}", "\n        ".join(js))
        .replace("{{CLIP_FROM}}", clip_from)
        .replace("{{CLIP_TO}}", clip_to)
        .replace("{{UX}}", str(ux)).replace("{{UY}}", str(uy))
        .replace("{{LX}}", str(lx)).replace("{{LY}}", str(ly))
        .replace("{{PW}}", str(PANEL_W)).replace("{{PH}}", str(PANEL_H))
    )
    (ROOT / "compositions/demo.html").write_text(html)


# ------------------------------------------------------------------ sound design (absolute seconds)
def sfx_list():
    D = DEMO0
    P, SO, IM, TR, OU = 76.8, 93.6, 108.0, 124.8, 146.4
    s = []
    for c in (12.0, P, SO, IM, TR):
        s.append(("whoosh", c - 0.5, 0.42))
    # hook: punchy beat changes
    s += [("pop", 0.45, 0.3), ("whoosh-soft", 1.0, 0.3), ("whoosh-soft", 2.0, 0.35), ("pop", 2.6, 0.3),
          ("whoosh-soft", 4.1, 0.35), ("pop", 4.75, 0.3), ("click", 6.35, 0.55), ("success", 6.6, 0.45),
          ("whoosh", 8.25, 0.35), ("thud", 8.62, 0.45)]
    # demo
    s += [
        ("whoosh-soft", D + 0.3, 0.35), ("pop", D + 3.05, 0.25), ("pop", D + 5.0, 0.25),
        ("pop", D + 8.15, 0.3), ("tick", D + 9.55, 0.35),
        ("key", D + 11.12, 0.5), ("key", D + 11.22, 0.5), ("click", D + 13.65, 0.55),
        ("pop", D + 15.0, 0.28), ("whoosh-soft", D + 15.3, 0.25), ("pop", D + 16.05, 0.3),
        ("click", D + 19.63, 0.55),
        ("whoosh-soft", D + 21.15, 0.4), ("click", D + 22.85, 0.6), ("pop", D + 23.8, 0.3),
        ("whoosh-soft", D + 24.25, 0.3), ("pop", D + 24.6, 0.25), ("thud", D + 25.5, 0.35), ("tick", D + 25.9, 0.4),
        ("ping", D + 26.05, 0.45), ("click", D + 33.25, 0.6),
        ("pop", D + 36.1, 0.28), ("whoosh-soft", D + 36.55, 0.3), ("tick", D + 37.5, 0.4),
        ("click", D + 39.15, 0.55), ("click", D + 42.5, 0.55),
        ("click", D + 47.25, 0.6), ("whoosh-soft", D + 47.35, 0.4), ("click", D + 49.0, 0.6),
        ("success", D + 49.75, 0.45), ("thud", D + 50.1, 0.3), ("click", D + 52.2, 0.5), ("pop", D + 52.75, 0.3),
        ("pop", D + 55.4, 0.28), ("whoosh-soft", D + 56.0, 0.3), ("tick", D + 56.95, 0.4),
        ("pop", D + 59.1, 0.3), ("success", D + 62.5, 0.4),
    ]
    for t in (4.52, 7.32, 9.66, 11.83, 13.54):
        s.append(("pop", P + t, 0.24))
    for t in (3.8, 5.5, 8.22, 9.68):
        s.append(("pop", SO + t, 0.26))
    s.append(("success", SO + 10.35, 0.3))
    for t in (3.1, 5.74, 9.62, 12.1):
        s.append(("pop", IM + t, 0.25))
    s += [("thud", TR + 3.1, 0.3), ("thud", TR + 5.55, 0.3), ("thud", TR + 12.28, 0.3),
          ("pop", TR + 7.85, 0.25), ("pop", TR + 8.9, 0.25),
          ("pop", TR + 14.2, 0.25), ("pop", TR + 16.95, 0.25),
          ("pop", OU + 0.55, 0.3)]
    return sorted(s, key=lambda x: x[1])


def music_lane():
    """Bed level: full between lines, ducked under the voice with short ramps."""
    hi, lo, ramp = 0.62, 0.2, 0.3
    windows = sorted((t, t + VO_DUR[k]) for k, t in VO)
    pts = [(0.0, 0.8), (0.3, 0.8)]
    for a, b in windows:
        pts.append((max(a - ramp, pts[-1][0] + 0.01), hi))
        pts.append((a, lo))
        pts.append((b, lo))
        pts.append((b + ramp, hi))
    pts.append((TOTAL - 1.5, 0.7))
    pts.append((TOTAL, 0.0))
    # merge overlapping ramps (gaps shorter than 2*ramp stay ducked)
    clean = []
    for t, v in pts:
        if clean and t <= clean[-1][0]:
            clean[-1] = (clean[-1][0], min(clean[-1][1], v))
            continue
        clean.append((t, v))
    return {"version": 1, "lanes": [{"target": "volume", "points": [{"t": round(t, 3), "v": v} for t, v in clean]}]}


def build_index():
    hosts = "\n      ".join(
        f'<div id="sc-{sid}" class="scene clip" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
        f'data-start="{r3(st)}" data-duration="{r3(du)}" data-track-index="1" data-width="1920" data-height="1080"></div>'
        for sid, st, du in SCENES
    )
    vo = "\n      ".join(
        f'<audio id="vo-{k}" src="assets/vo/{k}.wav" data-start="{r3(t)}" data-duration="{VO_DUR[k]}" data-track-index="20" data-volume="1"></audio>'
        for k, t in VO
    )
    sfx = "\n      ".join(
        f'<audio id="sfx-{i}" src="assets/sfx/{n}.wav" data-start="{r3(t)}" data-track-index="{40 + i}" data-volume="{v}"></audio>'
        for i, (n, t, v) in enumerate(sfx_list())
    )
    lane = json.dumps(music_lane(), separators=(",", ":"))
    music = (
        f'<audio id="music" src="assets/audio/music.wav" data-start="0" data-duration="{TOTAL}" data-track-index="30" '
        f"data-volume=\"1\" data-automation='{lane}'></audio>"
    )
    wipes = [(12.0, "#04143c"), (76.8, "#0a5cf5"), (93.6, "#0a5cf5"), (108.0, "#0a5cf5"), (124.8, "#04143c")]
    wipe_divs = "\n      ".join(
        f'<div class="wipe" id="wipe{i}" style="background:{c}"><div class="wipe-logo"></div></div>'
        for i, (_t, c) in enumerate(wipes)
    )
    wipe_js = "\n      ".join(
        f'tl.fromTo("#wipe{i}", {{ xPercent: 101 }}, {{ xPercent: 0, duration: 0.42, ease: "power3.in", immediateRender: false }}, {t - 0.42});\n'
        f'      tl.to("#wipe{i}", {{ xPercent: -101, duration: 0.46, ease: "power3.out" }}, {t + 0.04});'
        for i, (t, _c) in enumerate(wipes)
    )
    html = (ROOT / "scripts/index_template.html").read_text()
    html = (
        html.replace("{{TOTAL}}", str(TOTAL)).replace("{{HOSTS}}", hosts).replace("{{VO}}", vo)
        .replace("{{SFX}}", sfx).replace("{{MUSIC}}", music).replace("{{WIPES}}", wipe_divs).replace("{{WIPE_JS}}", wipe_js)
    )
    (ROOT / "index.html").write_text(html)


if __name__ == "__main__":
    build_demo()
    build_index()
    print("built demo.html + index.html")
