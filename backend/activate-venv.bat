@echo off
chcp 65001 >nul
echo ========================================
echo   QuantLife AI - 虚拟环境激活脚本
echo ========================================
echo.

if exist "venv\Scripts\activate.bat" (
    echo ✓ 虚拟环境已找到
    echo.
    echo 激活虚拟环境...
    call venv\Scripts\activate.bat
    echo.
    echo ✓ 虚拟环境已激活
    echo.
    echo 你现在可以运行:
    echo   - python test_data_loader.py    (测试数据获取)
    echo   - python test_simulation.py     (测试模拟引擎)
    echo   - python -m uvicorn app.main:app --reload  (启动服务器)
    echo.
) else (
    echo ✗ 错误: 虚拟环境不存在！
    echo.
    echo 请先创建虚拟环境:
    echo   python -m venv venv
    echo   pip install -r requirements.txt
    echo.
)
