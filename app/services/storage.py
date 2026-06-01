# app/services/storage.py
from pathlib import Path
import shutil

class StorageService:
    """
    负责文件目录、文件写入、生成可访问 URL 的“存储服务”
    """
    def __init__(self, files_dir: Path, public_prefix: str = "/files"):
        self.files_dir = files_dir
        self.public_prefix = public_prefix
        self.files_dir.mkdir(parents=True, exist_ok=True)

    def ensure_job_dir(self, job_id: str) -> Path:
        job_dir = self.files_dir / job_id
        job_dir.mkdir(parents=True, exist_ok=True)
        return job_dir

    def save_copy(self, src: Path, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)

    def public_url(self, path_in_files: Path) -> str:
        """
        把 files_dir 下的路径转换成 /files/... URL
        """
        # path_in_files 必须在 files_dir 内
        rel = path_in_files.relative_to(self.files_dir)
        return f"{self.public_prefix}/{rel.as_posix()}"