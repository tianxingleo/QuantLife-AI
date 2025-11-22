@echo off
chcp 65001 >nul
echo 正在启动 QuantLife AI 后端服务...
cd backend

:: 检查虚拟环境是否存在
if exist "venv\Scripts\activate.bat" (
    echo 激活虚拟环境...
    call venv\Scripts\activate.bat
    echo.
    echo ✓ 虚拟环境已激活
    echo.
) else (
    echo ⚠ 警告: 虚拟环境不存在，使用全局 Python
    echo 建议运行: python -m venv venv
    echo.
)

echo 启动 FastAPI 服务器...
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
