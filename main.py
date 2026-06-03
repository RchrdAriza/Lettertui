from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.containers import Grid
from textual.widgets import Header, Footer, Label, TabPane, TabbedContent
from UI.general.general import Portada, Info, Metadata


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
