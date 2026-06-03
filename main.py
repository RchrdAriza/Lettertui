import httpx
from PIL import Image
from io import BytesIO
from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.containers import Grid
from textual.widgets import Header, Footer, Label, Static, TabPane, TabbedContent
from textual.containers import Center
from API.tmdb import search_movies
from textual_image.widget import Image as textual_image

data = search_movies("superman")
pelicula = data["results"][0]
poster_path = pelicula["poster_path"]


class Poster(Static):
    async def on_mount(self) -> None:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://image.tmdb.org/t/p/w300{poster_path}")
            pilimage = Image.open(BytesIO(response.content))

            poster = textual_image(pilimage)

            await self.mount(poster)


class Portada(Widget):

    def on_mount(self) -> None:
        self.border_subtitle = "Portada"

    def compose(self) -> ComposeResult:
        yield Poster()


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


class Pestanas(Widget):
    def compose(self) -> ComposeResult:
        with TabbedContent(initial="pestana_inicio"):

            with TabPane("Inicio", id="pestana_inicio"):
                with Grid():
                    yield Portada()
                    yield Info()
                    yield Metadata()
            with TabPane("Configuración", id="pestana_config"):
                yield Label("Panel de Configuración")
                yield Label("Opción 1: [ ] Activar algo")
                yield Label("Opción 2: [ ] Otra opción")


class Lettertui(App):

    CSS_PATH = "tcss/style.tcss"

    BINDINGS = [
        ("d", "toggle_dark", "Modo oscuro"),
        ("q", "quit", "Salir")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Pestanas()
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = Lettertui()
    app.run()
