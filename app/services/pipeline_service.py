# app/services/pipeline_service.py
from dataclasses import dataclass
from pathlib import Path
import uuid

from .storage import StorageService

@dataclass
class ProcessResult:
    job_id: str
    preview_path: Path
    final_path: Path
    preview_url: str
    final_url: str

class PipelineService:
    """
    教学版流水线：先用“复制原图”模拟处理
    """
    def __init__(self, storage: StorageService):
        self.storage = storage

    def process(self, raw_path: str) -> ProcessResult:
        raw = Path(raw_path)
        if not raw.exists():
            raise FileNotFoundError(f"raw_path not exists: {raw}")

        job_id = "job_" + uuid.uuid4().hex[:8]
        job_dir = self.storage.ensure_job_dir(job_id)

        preview_path = job_dir / "preview.jpg"
        final_path = job_dir / "final.jpg"

        # 教学闭环：把原图复制为 preview/final
        self.storage.save_copy(raw, preview_path)
        self.storage.save_copy(raw, final_path)

        return ProcessResult(
            job_id=job_id,
            preview_path=preview_path,
            final_path=final_path,
            preview_url=self.storage.public_url(preview_path),
            final_url=self.storage.public_url(final_path),
        )