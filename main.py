from sys import argv
from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.containers import Grid
from textual.widgets import Header, Footer, Label, TabPane, TabbedContent, Button
from UI.general.general import Portada, Info, Metadata
from scraping.scrapping_main import LetterboxdProfile


class Pestanas(Widget):
    def __init__(self, usuario: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario

    def compose(self) -> ComposeResult:
        with TabbedContent(initial="pestana_inicio"):

            with TabPane("perfil", id="perfil"):
                yield Button(f"Buscar Perfil de {self.usuario}", id="btn_buscar")
                yield Label("Aqui va el perfil")

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

    def __init__(self):
        super().__init__()
        self.scrapper = LetterboxdProfile("maria_ig")

    CSS_PATH = "tcss/style.tcss"

    BINDINGS = [
        ("d", "toggle_dark", "Modo oscuro"),
        ("q", "quit", "Salir")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Pestanas(self.scrapper.usuario)
        yield Footer()

    async def on_mount(self) -> None:
        await self.scrapper.iniciarScrapeo()

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = Lettertui()
    app.run()
