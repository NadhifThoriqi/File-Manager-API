from fastapi import APIRouter

from ..service import storage

router = APIRouter(prefix="/storage", tags=["storage"])

@router.get("/info")
def get_storage_info():
    return storage.info()