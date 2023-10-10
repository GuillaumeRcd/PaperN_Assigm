from typing import Union
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

app = FastAPI()

class AddressRequest(BaseModel):
    text: str

stored_address = ""
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"], 
    allow_headers=["*"],
)


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

@app.post("/network/")
async def test(request: AddressRequest):
    global stored_address
    stored_address = request.text
    print(request.text)
    return {'message': f'Adresse reçue : {stored_address}'}


@app.get("/network/", response_model=dict)
async def get_network_data():
    global stored_address
    return {"message": "Données réseau obtenues avec succès", "address": stored_address}

@app.get("/proxy/")
async def proxy_address(address: str):
    print(address)
    if not address:
        raise HTTPException(status_code=400, detail="Address is required")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://api-adresse.data.gouv.fr/search/?q={address}")
            response.raise_for_status() 

        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching data") from e