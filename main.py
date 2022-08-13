import uvicorn
from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import geopandas as gpd
from shapely.geometry import Point

class Item(BaseModel):
    latitude: List[float] = []
    longitude: List[float] = []
    	

cpu_count = 4
API_LINK = '127.0.0.1:8000'
# app = FastAPI(openapi_url=None) # will close the swagger
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
    	
    	
def load_glb_shp():
    gpd.options.use_pygeos = False
    shp_file = 'data/gadm404_Level1.parquet'
    return gpd.read_parquet(shp_file)


async def pointinpolygon(gdf_globe, loc_lat, loc_lon):
    r_index = gdf_globe.sindex
    pt_latlon = Point(loc_lon, loc_lat)
    idx = r_index.query(pt_latlon, predicate="within").T

    if not idx:
        return {"longitude": loc_lon,
                "latitude": loc_lat,
                "State": "Ocean",
                "Country": "Ocean",
                }
    else:
        df_pt = gdf_globe[['State', 'Country']].iloc[idx].values.tolist()[0]
        return {"longitude": loc_lon,
                "latitude": loc_lat,
                "State": df_pt[0],
                "Country": df_pt[1],
                }


async def pointinpolygons(gdf_globe, locs:Item):
    loc_lats = locs.latitude
    loc_lons = locs.longitude
    gdf_locs = gpd.GeoSeries(gpd.points_from_xy(loc_lons, loc_lats))

    r_index = gdf_globe.sindex
    idx = r_index.query_bulk(gdf_locs, predicate="within").T

    land_points = gdf_locs.iloc[idx[:, 0]]
    lons = [ew_point.coords.xy[0][0] for ipt, ew_point in enumerate(land_points)]
    lats = [ew_point.coords.xy[1][0] for ipt, ew_point in enumerate(land_points)]

    df_land_points = gdf_globe[['State', 'Country']].iloc[idx[:, 1]]    
    df_land_points['latitude'] = lats
    df_land_points['longitude'] = lons
 
    return df_land_points[['longitude', 'latitude', "State", 'Country']].to_dict('records')


@app.get("/")
async def welcome() -> dict:
    return dict(message="Welcome to use point in polygon service.\n"
                        "Check geoinfo at the location of latitude and longitude"                        
                )


@app.get('/pip/')
async def api_pip(latlng: str = ''):
    latlng = [eval(i) for i in latlng.replace(' ', '').split()]
    loc_lon = latlng[0][1]
    loc_lat = latlng[0][0]

    if (loc_lat > 90.0) or (loc_lat < -90.0):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="latitude should be between 90 and -90.",
        )

    if (loc_lon > 180.0) or (loc_lon < -180.0):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="longitude should be between -180 and 180.",
        )

    return await pointinpolygon(gdf_glb, loc_lat, loc_lon)


@app.post('/pips/')
async def api_pips(args: Item):
    if args.latitude and args.longitude:
        if len(args.latitude) != len(args.longitude):
	        raise HTTPException(
	            status_code=status.HTTP_404_NOT_FOUND,
	            detail="The latitude and longitude should have the same length.",
	        )

        results = await pointinpolygons(gdf_glb, args)
        return results
    else:
        return {'Alert': 'Please provide latitude and longitude information'}


gdf_glb = load_glb_shp()


if __name__ == '__main__': 
    host, port = API_LINK.split(':')
    uvicorn.run(
        "main:app",
        host=host,
        port=int(port),
        factory=False,
        reload=False,
        loop='asyncio',
        workers=cpu_count,
    )
