import httpx
import os
from dotenv import load_dotenv


load_dotenv()

TMDB_TOKEN = os.getenv("TMDB_TOKEN")
BASE_URL = "https://api.themoviedb.org/3/"


def search_movies(query: str, page: int = 1, language: str = "es-CO"):
    with httpx.Client(
        base_url=BASE_URL,
        headers={
            "Authorization": f"Bearer {TMDB_TOKEN}",
            "accept": "application/json"
        }
    ) as client:
        response = client.get("/search/movie", params={
            "query": query,
            "language": language,
            "page": page,
            "include_adult": False
        })

        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    data = search_movies("Inception")
    resultado = data["results"][0]
# print(f"Total resultados: {data['results'][0]}")
# print(f"Total páginas: {data['total_pages']}")
    print(resultado["title"])
    print(resultado["poster_path"])
    print(resultado["release_date"])
