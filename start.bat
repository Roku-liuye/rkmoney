@echo off
chcp 65001 > nul
cls

echo ========================================
echo   rkmoney - 资产价值管理应用启动脚本
echo ========================================
echo.

REM 检查 Python 是否安装
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 未安装，请安装 Python 3.8+
    pause
    exit /b 1
)

REM 检查 Node.js 是否安装
node --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js 未安装，请安装 Node.js 20+
    pause
    exit /b 1
)

echo ✅ Python 版本: 
python --version 2>&1 | findstr /r "Python [0-9]"
echo.

echo ✅ Node.js 版本: 
node --version 2>&1
echo.

REM 启动后端
echo 🚀 正在启动后端服务...
cd backend

if not exist "venv" (
    echo 📦 创建虚拟环境...
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -r requirements.txt > nul 2>&1

echo 🔧 初始化数据库...
python -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine)" > nul 2>&1

echo ▶️  启动后端服务器 (http://localhost:8000)...
start "rkmoney-backend" uvicorn main:app --reload --host 0.0.0.0
cd ..

timeout /t 3 /nobreak > nul

REM 启动前端
echo 🚀 正在启动前端服务...
cd frontend

if not exist "node_modules" (
    echo 📦 安装前端依赖...
    call npm install
)

echo ▶️  启动前端开发服务器 (http://localhost:5173)...
start "rkmoney-frontend" npx vite --host 0.0.0.0 --port 5173
cd ..

echo.
echo ========================================
echo   ✅ 服务启动成功！
echo ========================================
echo   🌐 前端地址: http://localhost:5173
echo   🔌 后端地址: http://localhost:8000
echo   📖 API文档: http://localhost:8000/docs
echo ========================================
echo.
echo 💡 提示：后端和前端已在独立窗口中启动
echo.
pause
