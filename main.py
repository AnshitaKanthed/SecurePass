from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from subprocess import run, PIPE
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    """
    Serve the index.html file.
    """
    return FileResponse("static/index.html")

class EncryptionRequest(BaseModel):
    plaintext: str
    master_key: str

class DecryptionRequest(BaseModel):
    ciphertext: str
    master_key: str

@app.post("/encrypt/")
async def encrypt(request: EncryptionRequest):
    try:
        result = run(['python3', 'AES.py', request.master_key, request.plaintext, 'encrypt'], stdout=PIPE, stderr=PIPE, text=True)
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        return result.stdout
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/decrypt/")
async def decrypt(request: DecryptionRequest):
    try:
        result = run(['python3', 'AES.py', request.master_key, request.ciphertext, 'decrypt'], stdout=PIPE, stderr=PIPE, text=True)
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        return result.stdout.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
