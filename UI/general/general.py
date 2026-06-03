from textual_image.widget import Image as textual_image
from textual.widgets import Static
import httpx
from PIL import Image
from io import BytesIO
from API.tmdb import search_movies
from textual.app import ComposeResult
from textual.widget import Widget

data = search_movies("el viaje de chihiro")
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
