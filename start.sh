#!/bin/bash

echo "========================================"
echo "  rkmoney - 资产价值管理应用启动脚本"
echo "========================================"
echo ""

# 检查 Python 是否安装
if ! command -v python &> /dev/null; then
    echo "❌ Python 未安装，请安装 Python 3.8+"
    exit 1
fi

# 检查 Node.js 是否安装
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请安装 Node.js 20+"
    exit 1
fi

echo "✅ Python 版本: $(python --version 2>&1 | cut -d' ' -f2)"
echo "✅ Node.js 版本: $(node --version 2>&1 | cut -d' ' -f2)"
echo ""

# 启动后端
echo "🚀 正在启动后端服务..."
cd backend
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1

echo "🔧 初始化数据库..."
python -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine)" > /dev/null 2>&1

echo "▶️  启动后端服务器 (http://localhost:8000)..."
uvicorn main:app --reload &
BACKEND_PID=$!
cd ..

sleep 2

# 启动前端
echo "🚀 正在启动前端服务..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "📦 安装前端依赖..."
    npm install
fi

echo "▶️  启动前端开发服务器 (http://localhost:5173)..."
npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo "========================================"
echo "  ✅ 服务启动成功！"
echo "========================================"
echo "  🌐 前端地址: http://localhost:5173"
echo "  🔌 后端地址: http://localhost:8000"
echo "  📖 API文档: http://localhost:8000/docs"
echo "========================================"
echo ""
echo "💡 提示：按 Ctrl+C 可停止所有服务"
echo ""

# 等待用户中断
wait
