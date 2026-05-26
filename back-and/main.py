from fastapi import FastAPI, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Any

from app.api import folders, files, storage, pysystem

import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # --- DIJALANKAN SAAT STARTUP ---
    print("Aplikasi sedang berjalan, membuat tabel...")

    # Aplikasi mulai menerima request setelah ini
    yield
    
    # --- DIJALANKAN SAAT SHUTDOWN ---
    print("Aplikasi sedang dimatikan...")
    
# PENTING: Tambahkan root_path agar sinkron dengan Nginx /thorix/
app = FastAPI(root_path="/thorix", lifespan=lifespan) 

# === TAMBAHKAN INI (PENTING!) ===
# Jika tidak diinisialisasi di sini, middleware akan eror karena variabel belum ada saat dicek
app.state.is_lockdown = False
# ================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT", "PATCH"],
    allow_headers=["*"],
)

@app.middleware("http")
async def kunci_operasi_sistem(request: Request, call_next: Any):
    # Mengecek status lockdown dari state app
    if request.app.state.is_lockdown and request.method in ["POST", "PUT", "DELETE", "PATCH"]:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Server sedang bersiap untuk restart/shutdown. Operasi perubahan data dimatikan."
        )
    
    return await call_next(request)

# Root route untuk testing apakah aplikasi sudah "up"
@app.get("/")
def read_root():
    return {"status": "FastAPI is running", "path": "/thorix/"}

app.include_router(folders.router)
app.include_router(files.router)
app.include_router(storage.router)
app.include_router(pysystem.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=2026, reload=True) # nosec