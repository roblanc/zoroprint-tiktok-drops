"""Render the 7 educational carousels (1080 x 1350 JPG) from /home/claude/carousels.json."""
import json, html, re, os, io, sys
from playwright.sync_api import sync_playwright
from PIL import Image

D = "/home/claude/carousels"
A = "/tmp/claude-0/-home-claude/6efbe702-4a39-56d8-8441-0c2b7e542467/scratchpad/mac-carousel/a"
DATA = json.load(open("/home/claude/carousels.json"))


def acc(t):
    parts = re.split(r"\*(.+?)\*", t or "")
    return "".join(html.escape(p) if i % 2 == 0 else f'<span class="or">{html.escape(p)}</span>' for i, p in enumerate(parts))


CSS = open(f"{D}/style.css").read()


def slide_html(c, s, n, total):
    head = f'<div class="top"><div class="l"><img src="a/cat-mark-400.webp">ZoroPrint · <b>{html.escape(c["series"])}</b></div><div>{n:02d} / {total:02d}</div></div>'
    foot_r = "Swipe →" if n < total else "Save this"
    foot = f'<div class="foot"><div>@zoroprintdtfsoftware</div><div class="sw">{foot_r}</div></div>'
    t = s["type"]; body = ""; cls = "slide"
    if t == "cover":
        body = f'<div class="kick">{acc(s["kicker"])}</div><h1>{acc(s["title"])}</h1><div class="sub">{acc(s["sub"])}</div><div class="guide">Guide · zoroprint.com/guides</div>'
        cls += " cover"
    elif t in ("list", "steps"):
        items = "".join(
            f'<div class="it">{"<div class=num>%d</div>" % (k+1) if t=="steps" else "<div class=dot></div>"}<div><div class="t">{acc(i["t"])}</div><div class="d">{acc(i["d"])}</div></div></div>'
            for k, i in enumerate(s["items"]))
        body = f'<h2>{acc(s["title"])}</h2><div class="items n{len(s["items"])}">{items}</div>'
    elif t == "stat":
        body = f'<div class="kick">{acc(s["kicker"])}</div><div class="big">{acc(s["big"])}</div><div class="label">{acc(s["label"])}</div><div class="note">{acc(s["note"])}</div>'
        cls += " stat"
    elif t == "compare":
        L = "".join(f"<li>{acc(x)}</li>" for x in s["left"]["items"])
        R = "".join(f"<li>{acc(x)}</li>" for x in s["right"]["items"])
        body = (f'<h2>{acc(s["title"])}</h2><div class="cmp"><div class="col bad"><div class="cl">✕ {acc(s["left"]["label"])}</div><ul>{L}</ul></div>'
                f'<div class="col good"><div class="cl">✓ {acc(s["right"]["label"])}</div><ul>{R}</ul></div></div>')
    elif t == "tip":
        body = f'<div class="kick">{acc(s["kicker"])}</div><div class="tipcard"><h2>{acc(s["title"])}</h2><div class="tb">{acc(s["body"])}</div></div>'
    elif t == "cta":
        cls += " end"
        body = (f'<div class="endbig">{acc(s["big"])}</div><div class="endline">{acc(s["line"])}</div>'
                f'<div class="offer"><div>Start free <span>NO CARD</span></div><div>Unlimited · $8 / month <span>SOLO</span></div><div>macOS · Windows · Linux <span>SAME APP</span></div></div>'
                f'<div class="url">zoroprint.com</div><div class="gl">Full guide: {html.escape(c["guide"].replace("https://",""))}</div>')
    return f'<section class="{cls}" id="s{n}"><div class="safe">{head}<div class="body">{body}</div>{foot}</div></section>'


def page(c):
    total = len(c["slides"])
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>' + "".join(slide_html(c, s, i+1, total) for i, s in enumerate(c["slides"])) + "</body></html>"


if __name__ == "__main__":
    os.makedirs(f"{D}/out", exist_ok=True)
    if not os.path.exists(f"{D}/a"): os.symlink(A, f"{D}/a")
    ids = sys.argv[1:]
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for c in DATA:
            if ids and c["id"] not in ids: continue
            f = f"{D}/{c['id']}.html"; open(f, "w").write(page(c))
            pg.goto("file://" + f); pg.wait_for_timeout(700)
            od = f"{D}/out/{c['id']}"; os.makedirs(od, exist_ok=True)
            for i in range(1, len(c["slides"]) + 1):
                ov = pg.evaluate(f"(()=>{{const b=document.querySelector('#s{i} .body');return [b.scrollHeight,b.clientHeight]}})()")
                if ov[0] > ov[1] + 2: print("OVERFLOW", c["id"], i, ov)
                png = pg.locator(f"#s{i}").screenshot()
                Image.open(io.BytesIO(png)).convert("RGB").save(f"{od}/slide-{i:02d}.jpg", quality=92)
            print("ok", c["id"])
        b.close()
