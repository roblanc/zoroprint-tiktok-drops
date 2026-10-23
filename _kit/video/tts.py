import json,sys,os,numpy as np,soundfile as sf
sys.path.insert(0,"/home/claude/videos")
from specs import VIDEOS,END
from kokoro_onnx import Kokoro
k=Kokoro("/home/claude/tts/kokoro-v1.0.onnx","/home/claude/tts/voices-v1.0.bin")
VOICE=os.environ.get("VOICE","af_heart"); SPEED=float(os.environ.get("SPEED","1.06"))
def trim(a,sr,th=0.012):
    idx=np.where(np.abs(a)>th)[0]
    if not len(idx): return a
    s=max(0,idx[0]-int(0.03*sr)); e=min(len(a),idx[-1]+int(0.06*sr)); return a[s:e]
ONLY=sys.argv[1:]
out=json.load(open("/home/claude/videos/vo.json")) if ONLY else {}
for v in VIDEOS:
    if ONLY and v["id"] not in ONLY: continue
    d=f"/home/claude/videos/{v['id']}/assets/vo"; os.makedirs(d,exist_ok=True)
    lines=[("hook",v["hook_vo"],v["hook_vo"])]+[(f"s{i}",sh.get("say",sh["vo"]),sh["vo"]) for i,sh in enumerate(v["shots"])]+[("end",END["say"],END["text"])]
    res=[]
    for name,say,text in lines:
        a,sr=k.create(say,voice=VOICE,speed=SPEED,lang="en-us"); a=trim(a,sr)
        sf.write(f"{d}/{name}.wav",a,sr); res.append({"name":name,"text":text,"dur":round(len(a)/sr,3)})
    out[v["id"]]=res; print(v["id"],[(r["name"],r["dur"]) for r in res],flush=True)
json.dump(out,open("/home/claude/videos/vo.json","w"),indent=1)
