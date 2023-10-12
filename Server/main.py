from typing import Union
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import pyproj
import pandas as pd
from geopy.distance import geodesic as GD
import dask.dataframe as dd

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
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

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


def lamber93_to_gps(row):
    lambert = pyproj.Proj(
        "+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
    )
    wgs84 = pyproj.Proj("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")
    lon, lat = pyproj.transform(lambert, wgs84, row["x"], row["y"])
    return lon, lat


df = pd.read_csv(
    # "data/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv", delimiter=";"
    "data/test.csv", delimiter=";"
)

# dask_df = dd.from_pandas(df, npartitions=8)

# dask_df = dask_df.compute()

# dask_df[["lon", "lat"]] = dask_df.apply(
#     lambda row: lamber93_to_gps(row), axis=1, result_type="expand"
# )
df[["lon", "lat"]] = df.apply(
    lambda row: lamber93_to_gps(row), axis=1, result_type="expand"
)


@app.post("/coverage")
async def get_network_coverage(address_data: AddressData):
    print(address_data)
    user_point = (address_data.long, address_data.lat)
    result = {}

    operator_mapping = {20801: "Orange", 20810: "SFR", 20815: "Free", 20820: "Bouygues"}

    for index, row in df.iterrows():
        x = row["x"]
        y = row["y"]
        operator_code = row["Operateur"]
        operator_name = operator_mapping.get(operator_code)
        tested_Point = (row["lon"], row["lat"])

        if GD(user_point, tested_Point).km < 1:
            result[operator_name] = {"2G": False, "3G": False, "4G": False}
            result[operator_name]["2G"] = bool(row["2G"])
            result[operator_name]["3G"] = bool(row["3G"])
            result[operator_name]["4G"] = bool(row["4G"])

    return result


# def lamber93_to_gps(x, y):
#     lambert = pyproj.Proj(
#         "+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
#     )
#     wgs84 = pyproj.Proj("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")
#     long, lat = pyproj.transform(lambert, wgs84, x, y)
#     return long, lat
