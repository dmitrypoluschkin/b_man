from fastapi import FastAPI, HTTPException, Path, Query
from schemas import GenreURLChoices, BandBase, BandCreate, BandWithID
from typing import Annotated

app = FastAPI()


BANDS = [
    {"id": 1, "name": "The Kinks", "genre": "Rock"},
    {"id": 2, "name": "Aphex Twin", "genre": "Electronic"},
    {"id": 3, "name": "Black Sabbath", "genre": "Metal", "albums": [{
        "title": "Master of Reality", "release_date": "1971-07-21"
    }]},
    {"id": 4, "name": "Wu-Tang Clan", "genre": "Hip-Hop"},
    {"id": 5, "name": "The Kiss", "genre": "Rock"},
]


@app.get("/bands")
async def bands(genre: GenreURLChoices | None = None, q: Annotated[str | None, Query(max_length=10)] = None) -> list [BandWithID]:

    band_list = [BandWithID(**b) for b in BANDS]

    if genre:
        band_list = [
            b for b in band_list if b.genre.value.lower() == genre.value
        ]

    if q:
        band_list = [
            b for b in band_list if q.lower() in b.name.lower()
        ]

    return band_list


@app.get("/bands/{band_id}")
async def band(band_id: Annotated[int, Path(title="The band ID")]) -> BandWithID:
    band = next((BandWithID(**b) for b in BANDS if b["id"] == band_id), None)
    if band == None:
        # return status code 404
        raise HTTPException(status_code=404, detail="Band not found")
    return band


@app.get("/bands/genre/{genre}")
async def band_genre(genre: GenreURLChoices) -> list[dict]:
    return [
        b for b in BANDS if b["genre"].lower() == genre.value
        ]


@app.post("/bands")
async def create_band(band_data: BandCreate) -> BandWithID:
    id = BANDS[-1]['id'] + 1
    band = BandWithID(id=id, **band_data.model_dump()).model_dump()
    BANDS.append(band)
    return band