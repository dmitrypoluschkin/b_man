from fastapi import FastAPI, HTTPException

app = FastAPI()


BANDS = [
    {"id": 1, "name": "Aria", "genre": "Rock"},
    {"id": 2, "name": "Aphex Twin", "genre": "Electronic"},
    {"id": 3, "name": "Slowdive", "genre": "Shoegaza"},
    {"id": 4, "name": "Wu-Tang Clan", "genre": "Hip Hop"}
]


@app.get("/bands")
async def bands() -> list [dict]:
    return BANDS


@app.get("/bands/{band_id}")
async def about(band_id: int) -> dict:
    band = next((b for b in BANDS if b["id"] == band_id), None)
    if band == None:
        # return status code 404
        raise HTTPException(status_code=404, detail="Band not found")
    return band