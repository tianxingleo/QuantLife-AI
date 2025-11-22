@echo off
chcp 65001 >nul
echo ========================================
echo   QuantLife AI - 虚拟环境设置脚本
echo ========================================
echo.

if exist "venv" (
    echo ⚠ 警告: 虚拟环境已存在
    echo.
    set /p "choice=是否删除并重新创建? (y/N): "
    if /i not "%choice%"=="y" (
        echo 取消操作
        pause
        exit /b 0
    )
    echo.
    echo 删除现有虚拟环境...
    rmdir /s /q venv
    echo ✓ 删除完成
    echo.
)

echo 步骤 1/3: 创建虚拟环境...
python -m venv venv
echo ✓ 虚拟环境创建完成
echo.

echo 步骤 2/3: 升级 pip...
venv\Scripts\python.exe -m pip install --upgrade pip
echo ✓ pip 升级完成
echo.

echo 步骤 3/3: 安装项目依赖...
venv\Scripts\python.exe -m pip install -r requirements.txt
echo.
echo ========================================
echo   ✓ 安装完成！
echo ========================================
echo.
echo 下一步:
echo   1. 运行 activate-venv.bat 激活虚拟环境
echo   2. 或直接运行 ..\start-backend.bat 启动服务
echo.
pause
