from typing import Union
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import pyproj
import pandas as pd
from shapely.geometry import Point

app = FastAPI()


class AddressRequest(BaseModel):
    text: str


class AddressData(BaseModel):
    label: str
    value: str
    x: float
    y: float
    long: float
    lat: float


stored_address = ""

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# @app.post("/network/")
# async def test(request: AddressRequest):
#     global stored_address
#     stored_address = request.text
#     print(request.text)
#     return {"message": f"Adresse reçue : {stored_address}"}


# @app.get("/network/", response_model=dict)
# async def get_network_data():
#     global stored_address
#     return {"message": "Données réseau obtenues avec succès", "address": stored_address}


@app.get("/proxy/")
async def proxy_address(address: str):
    # print(address)
    if not address:
        raise HTTPException(status_code=400, detail="Address is required")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api-adresse.data.gouv.fr/search/?q={address}"
            )
            response.raise_for_status()

        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while fetching data"
        ) from e


df = pd.read_csv(
    # "data/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv", delimiter=";"
    "data/test.csv", delimiter=";"
)


@app.post("/coverage")
async def get_network_coverage(address_data: AddressData):
    print(address_data)
    user_point = Point(address_data.long, address_data.lat)
    rayon = 10
    result = {}
    
    operator_mapping = {
        20801: "Orange",
        20810: "SFR",
        20815: "Free",
        20820: "Bouygues"
    }
    
    for index, row in df.iterrows():
        x = row['x']
        y = row['y']
        operator_code = row['Operateur']
        operator_name = operator_mapping.get(operator_code)

        lon, lat = lamber93_to_gps(x, y)
        cercle = Point(lon, lat).buffer(rayon)
        
        if cercle.intersects(user_point) :
            result[operator_name] = {"2G": False, "3G": False, "4G": False}
            result[operator_name]["2G"] = bool(row['2G'])
            result[operator_name]["3G"] = bool(row['3G'])
            result[operator_name]["4G"] = bool(row['4G'])

    return result


def lamber93_to_gps(x, y):
    lambert = pyproj.Proj(
        "+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
    )
    wgs84 = pyproj.Proj("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")
    long, lat = pyproj.transform(lambert, wgs84, x, y)
    return long, lat
