from fastapi import APIRouter, Path, File, Query, Body, UploadFile, Depends

from ..service import files

router = APIRouter(prefix="/files", tags=["files"])

@router.get("")
def show_files(
    path: str = Query(default=".", description="Path dari folder yang ingin ditampilkan isinya"),
    password: bool = Depends(files.key)
):
    return files.lists(path, root= password)

@router.post("/upload")
def upload_file(
    upload_file: UploadFile = File(..., description="File yang ingin diupload"),
    path: str = Query(default=".", description="Path tujuan untuk file yang diupload"),
    password: bool = Depends(files.key)
):
    return files.upload(upload_file, path, root= password)

@router.put("/{file_id:str}")
def update_file(
    file_id: str = Path(..., description="ID dari file yang ingin diedit"),
    new_name: str = Body(..., description="Nama baru untuk file"),
    password: bool = Depends(files.key)
):
    return files.rename(file_id, new_name, root= password)

@router.delete("/{file_id:str}")
def delete_file(
    file_id: str=Path(..., description="ID dari file yang ingin dihapus"),
    password: bool = Depends(files.key)
):
    return files.delete(file_id, root= password)

@router.get("/{id:str}/download")
def download_file(
    id: str=Path(..., description="ID dari file yang ingin diunduh"),
    preview: bool = Query(default=False, description="Jika true, hanya mengembalikan preview (thumbnail) dari file"),
    password: bool = Depends(files.key)
):
    return files.download(id, preview=preview, root= password)

@router.get("/{id:str}/thumbnail")
def get_thumbnail(
    id: str=Path(..., description="ID dari file yang ingin ditampilkan thumbnail-nya"),
    password: bool = Depends(files.key)
):
    return files.thumbnail(id, root= password)