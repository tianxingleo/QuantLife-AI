@echo off
echo 正在启动 QuantLife AI 后端服务...
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
