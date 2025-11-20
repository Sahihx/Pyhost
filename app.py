from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from jobs_manager import JobManager
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
job_manager = JobManager()

# Load language settings
with open("lang.json", "r", encoding="utf-8") as f:
    LANGS = json.load(f)

LANG = "en"  # default

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "jobs": job_manager.list_jobs(),
        "lang": LANG,
        "texts": LANGS[LANG]
    })

@app.post("/run")
async def run_code(code: str = Form(...)):
    job_id = job_manager.start_job(code)
    return JSONResponse({"status": "started", "job_id": job_id})

@app.post("/stop")
async def stop_job(job_id: int = Form(...)):
    success = job_manager.stop_job(job_id)
    return JSONResponse({"status": "stopped" if success else "not_found"})

@app.get("/status/{job_id}")
async def job_status(job_id: int):
    return JSONResponse(job_manager.get_status(job_id))

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8443,
        ssl_certfile="cert/cert.pem",
        ssl_keyfile="cert/key.pem"
    )
  
