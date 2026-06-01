# app/routers/pipeline.py
from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from fastapi import UploadFile, File
from pathlib import Path
import uuid

router = APIRouter(prefix="/pipeline/v2", tags=["pipeline"])

class ProcessReq(BaseModel):
    template_code: str = Field(..., description="模板编码，例如 tpl_us_ny")
    raw_path: str = Field(..., description="本地原图路径（教学版先用本地路径模拟）")
    session_id: str = Field(..., description="会话ID")
    attempt_index: int = Field(0, description="第几次尝试，默认0")

@router.post("/process", summary="图片处理流水线接口（教学版）")
def process(req: ProcessReq, request: Request):
    pipeline = request.app.state.pipeline_service
    result = pipeline.process(req.raw_path)

    return {
        "code": "SUCCESS",
        "message": "processed (demo copy raw to preview/final)",
        "session_id": req.session_id,
        "template_code": req.template_code,
        "attempt_index": req.attempt_index,
        "job_id": result.job_id,
        "preview_url": result.preview_url,
        "final_url": result.final_url,
    }

@router.post("/upload", summary="上传原图（教学版）")
def upload(request: Request, file: UploadFile = File(...)):
    storage = request.app.state.storage_service

    raw_job = "raw_" + uuid.uuid4().hex[:8]
    job_dir = storage.ensure_job_dir(raw_job)
    raw_path = job_dir / file.filename

    # 保存上传文件
    raw_path.write_bytes(file.file.read())

    return {
        "code": "SUCCESS",
        "raw_path": str(raw_path),
        "raw_url": storage.public_url(raw_path),
    }