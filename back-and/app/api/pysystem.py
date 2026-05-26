# api.py
from fastapi import APIRouter, HTTPException, Request
import asyncio

from ..service.pysystem import system

router = APIRouter(prefix="/system", tags=["System Control"])

@router.post("/{aksi}")
async def pemicu_sistem(aksi: str, request: Request):
    if aksi not in ["reboot", "shutdown"]:
        raise HTTPException(status_code=400, detail="Aksi harus 'reboot' atau 'shutdown'")
    
    # Ambil objek app utama dari request
    app_utama = request.app
    
    # Jalankan di background, oper aksi dan objek app-nya
    asyncio.create_task(system(aksi, app_utama))
    
    return {"message": f"Server akan {aksi} dalam 5 detik. Mode baca-saja (GET) diaktifkan."}