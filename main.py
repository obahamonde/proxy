import os
from aiofauna import AioApp, AioClient, AioModel, jsonify, q, Request, Response, sse_response, render_template, Optional as O
from pydantic import Field
from geocoder import ip as geo_ip
from api.utils import get_ip
from dotenv import load_dotenv

load_dotenv(
)

FAUNA_SECRET = os.getenv("FAUNA_SECRET")

client = AioClient(FAUNA_SECRET)

class GeoModel(AioModel):
    ip:O[str] = Field(default=None, index=True)
    loc:O[str] = Field(default=None, index=True)
    city:O[str] = Field(default=None, index=True)
    country:O[str] = Field(default=None, index=True)
    autonomous_system:O[str] = Field(default=None, index=True)
    lat:O[float] = Field(default=None, index=True)
    lon:O[float] = Field(default=None, index=True)
    
app = AioApp()


async def parse_geo(req:Request):
    """
    Gets the geo data from a request coalescing the IP addresses options"""
    
    ipaddr = get_ip(req)

    if ipaddr:
    
        obj = geo_ip(ipaddr).json["raw"]
        
        _geo = GeoModel(
            ip=obj.get("ip"),
            loc=obj.get("loc"),
            city=obj.get("city"),
            country=obj.get("country"),
            autonomous_system=obj.get("autonomous_system"),
            lat=obj.get("lat"),
            lon=obj.get("lon")
        )
        
        return await _geo.create()
    return None
    
@app.get("/")
async def index(req:Request)->Response:
    await GeoModel.provision()
    geo = await parse_geo(req)
    return render_template("index.html", geo=geo)    

async def creaete_app():
    await app.listen()