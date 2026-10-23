import asyncio,re
from playwright.async_api import async_playwright
class S:
    async def start(self):
        self.p=await async_playwright().start(); self.b=await self.p.chromium.launch()
        self.pg=await (await self.b.new_context(viewport={"width":1440,"height":900},device_scale_factor=2)).new_page()
        await self.pg.goto("https://zoroprint.com/app/studio",wait_until="domcontentloaded")
        await self.pg.wait_for_timeout(23000); await self.pg.keyboard.press("Escape"); await self.pg.wait_for_timeout(600)
        self.app=self.pg.frame_locator("iframe").first
        m=self.app.get_by_label(re.compile("Mirror print",re.I)).first
        if await m.is_checked(): await m.uncheck()
        await self.pg.wait_for_timeout(800)
        return self
    def btn(self,t): return self.app.locator("button",has_text=re.compile(rf"^\s*{t}\s*$")).first
    async def click(self,t,w=900): await self.btn(t).click(); await self.pg.wait_for_timeout(w)
    async def shot(self,path,clip=None): await self.pg.screenshot(path=path,clip=clip)
    async def stop(self): await self.b.close(); await self.p.stop()
