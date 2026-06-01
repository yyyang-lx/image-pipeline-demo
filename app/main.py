# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import FILES_DIR, SERVICE_VERSION
from app.services.storage import StorageService
from app.services.pipeline_service import PipelineService
from app.routers.pipeline import router as pipeline_router
from datetime import datetime

app = FastAPI(title="image-pipeline-demo", version=SERVICE_VERSION)

# 1) 静态文件挂载：/files -> ./data/files
app.mount("/files", StaticFiles(directory=str(FILES_DIR)), name="files")

# 2) 服务注册（模拟 image-pipeline 的服务注入）
storage_service = StorageService(files_dir=FILES_DIR, public_prefix="/files")
pipeline_service = PipelineService(storage=storage_service)
app.state.storage_service = storage_service
app.state.pipeline_service = pipeline_service

# 3) 路由注册
app.include_router(pipeline_router)

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "image-pipeline-demo",
        "version": SERVICE_VERSION,
        "files_dir": str(FILES_DIR),
    }

@app.on_event("startup")
def on_startup():
    print(f"[startup] {datetime.now().isoformat()} files_dir={FILES_DIR}")

@app.on_event("shutdown")
def on_shutdown():
    print(f"[shutdown] {datetime.now().isoformat()} bye")