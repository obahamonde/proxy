from fastapi import FastAPI, Request, HTTPException
from geocoder import ip
from starlette.responses import RedirectResponse

app=FastAPI()

@app.get("/{port}", response_class=RedirectResponse)
async def redirect(port: str):
    return RedirectResponse(f"http://localhost:{port}/")

@app.middleware("http")
async def geocode_ip(request: Request, call_next):
    connecting_ip = request.headers['cf-connecting-ip']
    x_forwarded_for = request.headers['x-forwarded-for']
    if x_forwarded_for:
        connecting_ip = x_forwarded_for
    try:
        location = ip(connecting_ip)
        request.state.location = location
    except:
        raise HTTPException(status_code=500, detail="Unable to geocode IP")
    response = await call_next(request)
    return response
