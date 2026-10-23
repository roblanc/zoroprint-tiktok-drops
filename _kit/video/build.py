"""Build one HyperFrames project per video from specs.py + vo.json.
Usage: python3 build.py [video-id ...]"""
import json, os, re, shutil, sys, html
sys.path.insert(0, "/home/claude/videos")
from specs import VIDEOS

ROOT = "/home/claude/videos"
VO = json.load(open(f"{ROOT}/vo.json"))
W, H = 1080, 1920
SX, SY, SW, SH = 40, 480, 1000, 720           # the stage (product window)
CAP_W, CAP_H = 2880, 1800
ORANGE, INK, PAPER = "#FF7A1A", "#0E1220", "#F7F8FA"


def acc(t):
    """*word* -> orange span; escape the rest."""
    parts = re.split(r"\*(.+?)\*", t)
    return "".join(html.escape(p) if i % 2 == 0 else f'<b>{html.escape(p)}</b>' for i, p in enumerate(parts))


def cam_for(rect, fill=1.0):
    rx, ry, rw, rh = rect
    s = min(SW / rw, SH / rh) * fill
    x = SW / 2 - (rx + rw / 2) * s
    y = SH / 2 - (ry + rh / 2) * s
    return round(x, 2), round(y, 2), round(s, 5)


def groups(text, maxc=26):
    """Phrase-sized caption groups: break at punctuation, else near maxc; never leave a 1-word orphan."""
    words = text.split()
    out, cur = [], []
    for w in words:
        cand = " ".join(cur + [w])
        if cur and len(cand) > maxc:
            out.append(cur); cur = [w]
        else:
            cur.append(w)
        if cur and cur[-1].endswith((".", "?", "!", ":", ",")) and len(" ".join(cur)) >= 10:
            out.append(cur); cur = []
    if cur: out.append(cur)
    # merge orphans into a neighbour when it fits
    i = 0
    while i < len(out):
        if len(out[i]) == 1 and len(out) > 1:
            j = i - 1 if i > 0 and not out[i-1][-1].endswith((".", "?", "!")) else (i + 1 if i + 1 < len(out) else i - 1)
            if len(" ".join(out[j] + out[i])) <= maxc + 3:
                out[j] = out[j] + out[i] if j < i else out[i] + out[j]; out.pop(i); continue
        i += 1
    return [" ".join(g) for g in out]


def build(v):
    vid = v["id"]; d = f"{ROOT}/{vid}"; os.makedirs(f"{d}/assets", exist_ok=True)
    for f in os.listdir(f"{ROOT}/common"):
        shutil.copy(f"{ROOT}/common/{f}", f"{d}/assets/{f}")
    vo = {r["name"]: r for r in VO[vid]}
    used = set()
    for sh in v["shots"]:
        used.add(sh["img"]); sh.get("img2") and used.add(sh["img2"])
    for u in used:
        shutil.copy(f"{ROOT}/caps/{u}.png", f"{d}/assets/{u}.png")

    els, tw, audio, caps = [], [], [], []
    def T(s): tw.append(s)
    def clip(id_, start, dur, track, inner, cls="", style=""):
        els.append(f'<div id="{id_}" class="clip {cls}" data-start="{start:.3f}" data-duration="{dur:.3f}" data-track-index="{track}" style="{style}">{inner}</div>')
    def vo_at(name, t):
        r = vo[name]
        audio.append(f'<audio id="vo-{name}" class="clip" src="assets/vo/{name}.wav" data-start="{t:.3f}" data-duration="{r["dur"]:.3f}" data-track-index="20" data-volume="1"></audio>')
        gs = groups(r["text"]); total = sum(len(g) for g in gs); tt = t
        for g in gs:
            gd = r["dur"] * len(g) / total
            caps.append((tt, max(gd, 0.35), g)); tt += gd
        return r["dur"]
    sfx_n = [0]
    def sfx(name, t, vol, dur):
        sfx_n[0] += 1
        audio.append(f'<audio id="sfx{sfx_n[0]}" class="clip" src="assets/{name}.mp3" data-start="{max(t,0):.3f}" data-duration="{dur}" data-track-index="21" data-volume="{vol}"></audio>')

    # ---------- HOOK ----------
    t = 0.0
    hd = 0.25 + vo["hook"]["dur"] + 0.3
    lines = "".join(f'<div class="hl"><span class="hli" id="hl{i}">{acc(l)}</span></div>' for i, l in enumerate(v["hook"]))
    clip("hook", 0, hd, 2, f'<div class="kick" id="hook-kick">ZOROPRINT · {html.escape(v["kicker"])}</div><div class="hlines">{lines}</div><div class="bar" id="hook-bar"></div>', "scene")
    T('tl.fromTo("#hook-kick",{opacity:0,y:-16},{opacity:1,y:0,duration:0.35,ease:"power3.out"},0.0);')
    for i in range(len(v["hook"])):
        T(f'tl.fromTo("#hl{i}",{{yPercent:110}},{{yPercent:0,duration:0.55,ease:"power4.out"}},{0.05+i*0.11:.2f});')
    T('tl.fromTo("#hook-bar",{scaleX:0},{scaleX:1,duration:0.7,ease:"expo.out"},0.45);')
    T(f'tl.to(".hlines",{{y:-40,opacity:0,duration:0.3,ease:"power2.in"}},{hd-0.3:.2f});')
    vo_at("hook", 0.25)
    t = hd

    # ---------- STAGE ----------
    stage_start = t
    shot_html, title_html = [], []
    for i, sh in enumerate(v["shots"]):
        key = f"s{i}"; dur = 0.25 + vo[key]["dur"] + 0.35; dur = max(dur, 2.3)
        st = t
        sid = f"shot{i}"
        cams = sh.get("cam", [(0, 0, CAP_W, CAP_H)])
        c0 = cam_for(cams[0], 0.98 if cams[0][2] >= 2800 else 1.0)
        c1 = cam_for(cams[-1], 0.98 if cams[-1][2] >= 2800 else 1.0)
        inner = ""
        if sh.get("mac"):
            mw = 940; k = mw / 1600; mh = 966 * k
            mx, my = (SW - mw) / 2, (SH - mh) / 2 + 10
            scx, scy, scw, sch = mx + 165 * k, my + 51 * k, 1270 * k, 798 * k
            inner = (f'<div class="macwrap" id="{sid}-mac"><img class="macscreen" src="assets/{sh["img"]}.png" style="left:{scx:.1f}px;top:{scy:.1f}px;width:{scw:.1f}px;height:{sch:.1f}px">'
                     f'<img class="macbz" src="assets/macbook-pro-14-1600.webp" style="left:{mx:.1f}px;top:{my:.1f}px;width:{mw}px"></div>')
            T(f'tl.fromTo("#{sid}-mac",{{scale:0.9}},{{scale:1.04,duration:{dur:.2f},ease:"power1.out"}},{st:.3f});')
        else:
            ring = ""
            if sh.get("ring"):
                rx, ry, rw, rh = sh["ring"]; s1 = c1[2]
                ring = f'<div class="ring" id="{sid}-ring" style="left:{rx}px;top:{ry}px;width:{rw}px;height:{rh}px;border-width:{7/s1:.2f}px;border-radius:{18/s1:.2f}px"></div>'
            img2 = ""
            if sh.get("img2"):
                img2 = f'<img class="capimg" id="{sid}-b" src="assets/{sh["img2"]}.png">'
            inner = f'<div class="cam" id="{sid}-cam"><img class="capimg" id="{sid}-a" src="assets/{sh["img"]}.png">{img2}{ring}</div>'
            T(f'tl.set("#{sid}-cam",{{x:{c0[0]},y:{c0[1]},scale:{c0[2]}}},{st:.3f});')
            if len(cams) > 1:
                T(f'tl.fromTo("#{sid}-cam",{{x:{c0[0]},y:{c0[1]},scale:{c0[2]}}},{{x:{c1[0]},y:{c1[1]},scale:{c1[2]},duration:1.1,ease:"expo.inOut"}},{st+0.35:.3f});')
                drift_at = st + 1.45
            else:
                drift_at = st
            # slow drift so nothing is ever static
            T(f'tl.to("#{sid}-cam",{{scale:{c1[2]*1.035:.5f},x:{c1[0] - SW*0.0175:.2f},y:{c1[1] - SH*0.0175:.2f},duration:{max(dur-(drift_at-st),0.5):.2f},ease:"none"}},{drift_at:.3f});')
            ring_at = st + (1.5 if len(cams) > 1 else 0.45)
            if sh.get("ring"):
                T(f'tl.fromTo("#{sid}-ring",{{opacity:0,scale:1.12}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"}},{ring_at:.3f});')
                sfx("click", ring_at + 0.05, 1.2, 0.37)
            if sh.get("swap"):
                sw_at = st + 0.25 + vo[key]["dur"] * 0.62
                if sh.get("ring"): sw_at = max(sw_at, ring_at + 0.6)
                T(f'tl.fromTo("#{sid}-b",{{opacity:0}},{{opacity:1,duration:0.25,ease:"power1.inOut"}},{sw_at:.3f});')
                sfx("click", sw_at - 0.04, 1.0, 0.37)
            elif sh.get("img2"):
                T(f'tl.set("#{sid}-b",{{opacity:1}},{st:.3f});')
            if sh.get("wipe"):
                w0, w1 = st + 0.7, st + 0.7 + 1.6
                T(f'tl.fromTo("#{sid}-b",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:1.6,ease:"power2.inOut"}},{w0:.3f});')
                inner += f'<div class="wline" id="{sid}-line"></div>'
                T(f'tl.fromTo("#{sid}-line",{{x:0,opacity:1}},{{x:{SW},duration:1.6,ease:"power2.inOut"}},{w0:.3f});')
                T(f'tl.to("#{sid}-line",{{opacity:0,duration:0.2}},{w1:.3f});')
                la, lb = sh.get("labels", ["BEFORE", "AFTER"])
                inner += f'<div class="lab l" id="{sid}-la">{html.escape(la)}</div><div class="lab r" id="{sid}-lb">{html.escape(lb)}</div>'
                T(f'tl.fromTo("#{sid}-la",{{opacity:0,y:-10}},{{opacity:1,y:0,duration:0.3}},{st+0.3:.3f});')
                T(f'tl.to("#{sid}-la",{{opacity:0,duration:0.25}},{w1-0.4:.3f});')
                T(f'tl.fromTo("#{sid}-lb",{{opacity:0,y:-10}},{{opacity:1,y:0,duration:0.3}},{w1-0.3:.3f});')
                sfx("whoosh-short", w0, 0.5, 0.57)
            if sh.get("chip") and sh.get("ring"):
                rx, ry, rw, rh = sh["ring"]; x1, y1, s1 = c1
                sx_, sy_ = rx * s1 + x1, (ry + rh) * s1 + y1
                cy = sy_ + 18
                if cy > SH - 90: cy = ry * s1 + y1 - 86
                cx = min(max(sx_, 24), SW - 560)
                inner += f'<div class="chip" id="{sid}-chip" style="left:{cx:.0f}px;top:{cy:.0f}px">{html.escape(sh["chip"])}</div>'
                T(f'tl.fromTo("#{sid}-chip",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{ring_at+0.2:.3f});')
            if sh.get("chip") and not sh.get("ring"):
                inner += f'<div class="chip" id="{sid}-chip" style="left:24px;top:{SH-92}px">{html.escape(sh["chip"])}</div>'
                T(f'tl.fromTo("#{sid}-chip",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{st+1.2:.3f});')
            if i == 0 and v.get("note"):
                inner += f'<div class="note" id="{sid}-note">{html.escape(v["note"])}</div>'
        clip(sid, st, dur + (0.3 if i < len(v["shots"]) - 1 else 0), 40 + i, inner, "shot", "")
        T(f'tl.fromTo("#{sid}",{{opacity:0}},{{opacity:1,duration:0.22,ease:"power1.out"}},{st:.3f});')
        # title
        title_html.append((f"t{i}", st, dur, sh["title"]))
        vo_at(key, st + 0.25)
        t = st + dur
    stage_end = t
    stage_inner = "".join(shot_html)
    els.insert(0, f'<div id="stage" class="clip" data-start="{stage_start:.3f}" data-duration="{stage_end-stage_start:.3f}" data-track-index="3"></div>')
    T(f'tl.fromTo("#stage",{{opacity:0,scale:0.94,y:30}},{{opacity:1,scale:1,y:0,duration:0.55,ease:"expo.out"}},{stage_start:.3f});')
    sfx("whoosh-short", stage_start - 0.12, 0.7, 0.57)
    # kicker + titles above the stage
    clip("skick", stage_start, stage_end - stage_start, 5, f'<div class="kick">ZOROPRINT · {html.escape(v["kicker"])}</div>', "toplab")
    for (tid, st, dur, title) in title_html:
        clip(tid, st, dur, 6, f'<div class="ttl"><span id="{tid}-i">{acc(title)}</span></div>', "titlewrap")
        T(f'tl.fromTo("#{tid}-i",{{yPercent:105}},{{yPercent:0,duration:0.5,ease:"power4.out"}},{st+0.05:.3f});')

    # ---------- END ----------
    es = t; ed = 0.4 + vo["end"]["dur"] + 1.2
    end_inner = (f'<div class="end-in"><img class="endcat" id="end-cat" src="assets/cat-mark-400.webp">'
                 f'<div class="endword" id="end-word">zoroprint</div>'
                 f'<div class="endbig" id="end-big">Start free.</div>'
                 f'<div class="endchips" id="end-chips"><span>Unlimited · $8/month</span><span>macOS · Windows · Linux</span></div>'
                 f'<div class="endurl" id="end-url">zoroprint.com</div></div>')
    clip("end", es, ed, 8, end_inner, "endcard")
    T(f'tl.fromTo("#end",{{clipPath:"inset(100% 0 0 0)"}},{{clipPath:"inset(0% 0 0 0)",duration:0.45,ease:"expo.inOut"}},{es:.3f});')
    for j, el in enumerate(["#end-cat", "#end-word", "#end-big", "#end-chips", "#end-url"]):
        T(f'tl.fromTo("{el}",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.45,ease:"power3.out"}},{es+0.2+j*0.07:.3f});')
    sfx("whoosh-short", es - 0.1, 0.7, 0.57)
    vo_at("end", es + 0.4)
    total = es + ed

    # captions (not over the end card: it carries its own words)
    cap_html = []
    for j, (ct, cd, g) in enumerate(caps):
        if ct >= es: continue
        cap_html.append(f'<div id="cap{j}" class="clip cap" data-start="{ct:.3f}" data-duration="{cd:.3f}" data-track-index="9"><span id="cap{j}i">{html.escape(g)}</span></div>')
        T(f'tl.fromTo("#cap{j}i",{{opacity:0,y:12}},{{opacity:1,y:0,duration:0.12,ease:"power3.out"}},{ct:.3f});')

    doc = f'''<!doctype html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width={W}, height={H}">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
@font-face{{font-family:"Schibsted";src:url("assets/schibsted-grotesk.woff2") format("woff2");font-weight:400 900}}
@font-face{{font-family:"Plex";src:url("assets/plex-500.woff2") format("woff2");font-weight:500}}
@font-face{{font-family:"Plex";src:url("assets/plex-600.woff2") format("woff2");font-weight:600}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:{INK}}}
#root{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{INK};font-family:Schibsted,sans-serif;color:{PAPER}}}
#bg{{position:absolute;inset:-40px;background-image:radial-gradient(circle at 1px 1px,#222944 1.6px,transparent 1.8px);background-size:40px 40px}}
.scene{{position:absolute;inset:0}}
.kick{{position:absolute;left:56px;top:190px;font:600 28px Plex;letter-spacing:.14em;color:{ORANGE};background:{INK};padding:10px 16px;border:2px solid #2A3150;border-radius:12px}}
.hlines{{position:absolute;left:56px;right:40px;top:640px}}
.hl{{overflow:hidden;padding-bottom:6px}}
.hli{{display:inline-block;font-weight:880;font-size:148px;line-height:.98;letter-spacing:-.045em}}
.hli b,.ttl b{{color:{ORANGE};font-weight:inherit}}
.bar{{position:absolute;left:56px;top:1190px;width:300px;height:12px;background:{ORANGE};border-radius:6px;transform-origin:0 50%}}
#stage{{position:absolute;left:{SX}px;top:{SY}px;width:{SW}px;height:{SH}px;border-radius:36px;overflow:hidden;background:#0B0F1B;border:2px solid #2E3655;box-shadow:0 40px 100px rgba(0,0,0,.55)}}
.shot{{position:absolute;left:{SX}px;top:{SY}px;width:{SW}px;height:{SH}px;border-radius:36px;overflow:hidden}}
.cam{{position:absolute;left:0;top:0;width:{CAP_W}px;height:{CAP_H}px;transform-origin:0 0}}
.capimg{{position:absolute;left:0;top:0;width:{CAP_W}px;height:{CAP_H}px}}
.ring{{position:absolute;border-style:solid;border-color:{ORANGE};transform-origin:50% 50%}}
.wline{{position:absolute;left:0;top:0;width:6px;height:{SH}px;background:{ORANGE};margin-left:-3px}}
.lab{{position:absolute;top:22px;font:600 28px Plex;letter-spacing:.08em;background:{INK};color:{PAPER};padding:10px 14px;border-radius:10px;border:2px solid #2A3150}}
.lab.l{{left:22px}} .lab.r{{right:22px;color:{ORANGE};border-color:{ORANGE}}}
.chip{{position:absolute;font:600 28px Plex;background:{ORANGE};color:{INK};padding:12px 18px;border-radius:12px;white-space:nowrap}}
.note{{position:absolute;right:22px;bottom:22px;font:600 28px Plex;letter-spacing:.06em;background:{INK};color:{PAPER};padding:10px 14px;border-radius:10px;border:2px solid #2A3150}}
.macwrap{{position:absolute;inset:0;transform-origin:50% 55%}}
.macscreen,.macbz{{position:absolute}}
.toplab{{position:absolute;inset:0}}
.titlewrap{{position:absolute;left:0;top:0;width:{W}px}}
.ttl{{position:absolute;left:56px;right:40px;top:262px;overflow:hidden;padding-bottom:8px}}
.ttl span{{display:inline-block;font-weight:860;font-size:70px;line-height:1;letter-spacing:-.035em}}
.cap{{position:absolute;left:0;top:1225px;width:{W}px;text-align:center}}
.cap span{{display:inline-block;background:{INK};color:{PAPER};border-radius:16px;padding:12px 28px 18px;font-weight:800;font-size:60px;line-height:1.05;letter-spacing:-.02em;border:2px solid #2A3150}}
.endcard{{position:absolute;inset:0;background:{ORANGE};color:{INK}}}
.end-in{{position:absolute;left:72px;right:72px;top:300px}}
.endcat{{width:150px;height:150px}}
.endword{{font:600 34px Plex;letter-spacing:.2em;margin-top:18px;text-transform:uppercase}}
.endbig{{font-weight:900;font-size:190px;line-height:.9;letter-spacing:-.05em;margin-top:40px}}
.endchips{{display:flex;flex-direction:column;gap:16px;margin-top:56px}}
.endchips span{{align-self:flex-start;background:{INK};color:{PAPER};font-weight:780;font-size:46px;padding:18px 28px;border-radius:18px}}
.endurl{{font-weight:900;font-size:92px;letter-spacing:-.035em;margin-top:56px}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{total:.3f}" data-width="{W}" data-height="{H}">
<div id="bg"></div>
{chr(10).join(els)}
{chr(10).join(cap_html)}
{chr(10).join(audio)}
</div>
<script>
const tl = gsap.timeline({{paused:true}});
tl.fromTo("#bg",{{x:0,y:0}},{{x:-40,y:-40,duration:{total:.2f},ease:"none"}},0);
{chr(10).join(tw)}
window.__timelines["main"] = tl;
</script>
</body></html>'''
    open(f"{d}/index.html", "w").write(doc)
    json.dump({"$schema": "https://hyperframes.heygen.com/schema/hyperframes.json", "paths": {"assets": "assets"}, "media": {"autoProxy": True}}, open(f"{d}/hyperframes.json", "w"))
    json.dump({"name": vid, "private": True, "type": "module"}, open(f"{d}/package.json", "w"))
    print(vid, f"{total:.2f}s", len(caps), "captions")
    return total


if __name__ == "__main__":
    ids = sys.argv[1:] or [v["id"] for v in VIDEOS]
    for v in VIDEOS:
        if v["id"] in ids: build(v)
