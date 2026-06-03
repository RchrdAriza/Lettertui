from typing import Optional
from playwright.async_api import async_playwright
import asyncio


class LetterboxdProfile:
    def __init__(self, usuario: str):
        self.playwright = None
        self.browser = None
        self.page = None
        self.usuario = usuario

    async def iniciarScrapeo(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()

    async def obtener_perfil(self, usuario_id: Optional[str] = None):
        if usuario_id is None:
            usuario_id = self.usuario

        if not self.page:
            raise Exception("El scraper no ha sido iniciado")

        url = f"https://letterboxd.com/{usuario_id}/"
        await self.page.goto(url)

        nombreVisible = await self.page.locator("h1.person-display-name span.label").text_content()
        if nombreVisible:
            return nombreVisible.strip()

    async def cerrar(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()


async def main():
    scrapper = LetterboxdProfile()

    try:
        await scrapper.iniciarScrapeo()

        usuario = await scrapper.obtener_perfil("richard_a")
        print(f"Usuario extraido con exito: {usuario}")
    except Exception as e:
        print(f"Ocurrio un error: {e}")
        raise
    finally:
        await scrapper.cerrar()


if __name__ == "__main__":
    asyncio.run(main())
