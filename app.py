from fastapi import FastAPI, Request, HTTPException
from geocoder import ip
from starlette.responses import RedirectResponse, JSONResponse
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from nmap import PortScanner


templates = Jinja2Templates(directory="jinja2")
app=FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
sc = PortScanner()

@app.get("/app/{port}", response_class=RedirectResponse)
async def redirect(port: str):
    return RedirectResponse(f"http://54.88.107.129:{port}/")

@app.get('/')
async def root(req:Request):
    try:
        head = ip(req.headers['cf-connecting-ip']).json
        host = head['ip']
        res = sc.scan(host,)['nmap']['scaninfo']
        context = {
            **head['raw'],
            "ports":res['tcp']['services'].split(","),
            "request":req
        }
        return templates.TemplateResponse('index.jinja', context=context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


