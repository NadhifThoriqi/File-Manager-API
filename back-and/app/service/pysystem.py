from fastapi import FastAPI

# import os
import asyncio

# Pastikan fungsi matikan_linux berada di dalam file pyoff.py Anda
async def system(aksi: str, app: FastAPI):
    # Mengubah state lockdown melalui objek app yang dikirim dari API
    app.state.is_lockdown = True
    print(f"[SYSTEM] Server dikunci. Memulai hitung mundur 5 detik untuk {aksi}...")
    
    await asyncio.sleep(5)
    
    if aksi == "reboot":
        process = await asyncio.create_subprocess_shell("reboot")
        await process.communicate()
    elif aksi in ["shutdown", "poweroff"]:
        process = await asyncio.create_subprocess_shell("shutdown -h now")
        await process.communicate()
    else:
        app.state.is_lockdown = False
        print("[SYSTEM] Aksi tidak dikenal, lockdown dibuka kembali.")