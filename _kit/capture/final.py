import asyncio,re,json
from lib import S
OUT="/home/claude/videos/caps/"
SET="""([id,v])=>{const i=document.getElementById(id); if(i.type==='checkbox'){i.checked=v;} else {i.value=v;} i.dispatchEvent(new Event('input',{bubbles:true})); i.dispatchEvent(new Event('change',{bubbles:true})); return i.value}"""
boxes={}
async def bb(s,name,loc):
    try:
        b=await loc.bounding_box(); boxes[name]=[round(b['x']*2),round(b['y']*2),round(b['width']*2),round(b['height']*2)]
    except Exception as e: print("bbfail",name,str(e)[:80])
def row(a,id): return a.locator(f"#{id}").locator("xpath=ancestor::div[contains(@class,'slider') or contains(@class,'check') or contains(@class,'row')][1]")
async def main():
    s=await S().start(); a=s.app; pg=s.pg; f=pg.frames[1]
    async def shot(n): await s.shot(OUT+n+".png")
    await s.click("Print preview"); await shot("preview")
    await bb(s,"sheet",a.locator("canvas").first)
    await bb(s,"btn_print",s.btn("Print"))
    await bb(s,"btn_white",s.btn("White layer"))
    await s.click("White layer"); await shot("white")
    # colour tab
    await a.locator("button",has_text=re.compile(r"^\s*Colour\s*$")).first.click(); await pg.wait_for_timeout(700)
    await bb(s,"tab_colour",a.locator("button",has_text=re.compile(r"^\s*Colour\s*$")).first)
    # knockout
    await f.evaluate("()=>document.getElementById('knockoutBlack').scrollIntoView({block:'center'})"); await pg.wait_for_timeout(500)
    await s.click("White layer",900); await shot("ko_off_white"); await bb(s,"ko_off_row",row(a,"knockoutBlack"))
    await f.evaluate(SET,["knockoutBlack",True]); await pg.wait_for_timeout(1500); await shot("ko_on_white"); await bb(s,"ko_on_row",row(a,"knockoutBlack"))
    await bb(s,"ko_on_garment",a.get_by_text(re.compile("Use garment colour")).first)
    await s.click("Print preview",1200); await shot("ko_on_preview")
    await f.evaluate(SET,["knockoutBlack",False]); await pg.wait_for_timeout(1000)
    # soft hand
    await f.evaluate("()=>document.getElementById('softHand').scrollIntoView({block:'center'})"); await pg.wait_for_timeout(500)
    await s.click("White layer",900); await shot("soft0_white"); await bb(s,"soft_row0",row(a,"softHand"))
    await bb(s,"total",a.get_by_text(re.compile(r"^Total:")).first)
    await f.evaluate(SET,["softHand",40]); await pg.wait_for_timeout(1600); await shot("soft40_white"); await bb(s,"soft_row40",row(a,"softHand"))
    await f.evaluate(SET,["softHand",0]); await pg.wait_for_timeout(1000)
    # less white under dark
    await f.evaluate("()=>document.getElementById('whiteUnderDark').scrollIntoView({block:'center'})"); await pg.wait_for_timeout(500)
    await s.click("White layer",900); await shot("wud0_white"); await bb(s,"wud_row0",row(a,"whiteUnderDark"))
    await f.evaluate(SET,["whiteUnderDark",60]); await pg.wait_for_timeout(1600); await shot("wud60_white"); await bb(s,"wud_row60",row(a,"whiteUnderDark"))
    await f.evaluate(SET,["whiteUnderDark",0]); await pg.wait_for_timeout(1000)
    # ink limit
    await f.evaluate("()=>document.getElementById('inkLimit').scrollIntoView({block:'center'})"); await pg.wait_for_timeout(500)
    await s.click("Print preview",900); await shot("ink200"); await bb(s,"ink_row200",row(a,"inkLimit"))
    await f.evaluate(SET,["inkLimit",160]); await pg.wait_for_timeout(1500); await shot("ink160"); await bb(s,"ink_row160",row(a,"inkLimit"))
    await f.evaluate(SET,["inkLimit",200]); await pg.wait_for_timeout(800)
    # costs
    await a.locator("button",has_text=re.compile(r"^\s*Costs\s*$")).first.click(); await pg.wait_for_timeout(900); await shot("costs")
    await bb(s,"cost_job",a.get_by_text(re.compile("Job cost",re.I)).first.locator("xpath=ancestor::section[1] | ancestor::div[contains(@class,'card') or contains(@class,'panel') or contains(@class,'box')][1]").first)
    await bb(s,"cost_jobtitle",a.get_by_text(re.compile("Job cost",re.I)).first)
    await bb(s,"cost_used",a.get_by_text(re.compile("Ink really used",re.I)).first)
    # garment
    g=a.locator("button[title*='garment' i],button[aria-label*='garment' i],button[title*='shirt' i],button[aria-label*='shirt' i]").first
    await bb(s,"btn_garment",g)
    await g.click(); await pg.wait_for_timeout(1500); await shot("garment_centre")
    await bb(s,"garment_toggle",a.locator("button",has_text="Left chest").first)
    await a.locator("button",has_text="Left chest").first.click(); await pg.wait_for_timeout(1300); await shot("garment_left")
    await g.click(); await pg.wait_for_timeout(1000)
    # printer list
    pb=a.locator("button",has_text=re.compile("Epson L805")).first; await bb(s,"btn_printer",pb)
    await pb.click(); await pg.wait_for_timeout(1200); await shot("printers")
    await bb(s,"printer_menu",a.get_by_text(re.compile("Choose printer")).first.locator("xpath=ancestor::div[2]"))
    json.dump(boxes,open(OUT+"boxes.json","w"),indent=1); print(json.dumps(boxes))
    await s.stop()
asyncio.run(main())
