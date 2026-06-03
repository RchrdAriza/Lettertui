import httpx
from PIL import Image
from io import BytesIO
from textual.app import App, ComposeResult
from textual.widget import Widget
from textual_imageview.viewer import ImageViewer
from textual.containers import Grid
from textual.widgets import Header, Footer, Static
from API.tmdb import search_movies

data = search_movies("inception")
pelicula = data["results"][0]
poster_path = pelicula["poster_path"]


class PortadaImagen(Static):

    def compose(self) -> ComposeResult:
        placeholder = Image.new("RGB", (1, 1))
        yield ImageViewer(placeholder)

    async def on_mount(self) -> None:
        self.loading = True
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://image.tmdb.org/t/p/w300{poster_path}")
            imagen = Image.open(BytesIO(response.content))

        viewer = self.query_one(ImageViewer)
        await viewer.remove()
        await self.mount(ImageViewer(imagen))
        self.loading = False


class Portada(Widget):

    def on_mount(self) -> None:
        self.border_subtitle = "Portada"

    def compose(self) -> ComposeResult:
        yield PortadaImagen()


class Info(Static):

    def on_mount(self) -> None:
        self.border_subtitle = "Info"

    def compose(self) -> ComposeResult:
        yield Static("Info")


class Metadata(Static):

    def on_mount(self) -> None:
        self.border_title = "Metadata"

    def compose(self) -> ComposeResult:
        yield Static("Metadata")


class Lettertui(App):

    CSS_PATH = "tcss/style.tcss"

    BINDINGS = [
        ("d", "toggle_dark", "Modo oscuro"),
        ("q", "quit", "Salir")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Grid():
            yield Portada()
            yield Info()
            yield Metadata()
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = Lettertui()
    app.run()
