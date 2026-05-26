from .files import directory

import shutil

def info():
    disk = shutil.disk_usage(directory())
    return {
        "total_bytes": disk.total,
        "used_bytes":  disk.used,
        "free_bytes":  disk.free
    }