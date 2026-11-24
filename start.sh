#!/bin/bash

# 云端 Agent 助手工作台 - 本地测试脚本

echo "🚀 云端 Agent 助手工作台 - 本地测试脚本"
echo "================================================"

# 检查依赖
echo ""
echo "📋 检查依赖..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 未安装"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ Node.js/npm 未安装"
    exit 1
fi

echo "✅ Python 3: $(python3 --version)"
echo "✅ Node.js: $(node --version)"
echo "✅ npm: $(npm --version)"

# 启动后端
echo ""
echo "🔧 启动后端服务..."
cd backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "   创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

# 安装依赖
echo "   安装 Python 依赖..."
pip install -q -r requirements.txt

# 创建 .env 文件（如果不存在）
if [ ! -f ".env" ]; then
    echo "   创建 .env 文件..."
    cp .env.example .env
fi

# 启动后端
echo "   启动 Flask 应用..."
python app.py &
BACKEND_PID=$!

cd ..

# 等待后端启动
echo "   等待后端启动..."
sleep 3

# 验证后端
echo ""
echo "🔍 验证后端..."
if curl -s http://localhost:5000/api/health > /dev/null; then
    echo "✅ 后端服务运行正常"
else
    echo "❌ 后端服务启动失败"
    kill $BACKEND_PID
    exit 1
fi

# 启动前端
echo ""
echo "🎨 启动前端服务..."
cd frontend

echo "   安装 npm 依赖..."
npm install -q

echo "   启动 Vite 开发服务器..."
npm run dev &
FRONTEND_PID=$!

cd ..

# 等待前端启动
sleep 5

echo ""
echo "================================================"
echo "✅ 应用已启动！"
echo ""
echo "📱 前端：http://localhost:3000"
echo "🔗 后端：http://localhost:5000"
echo "📊 API：http://localhost:5000/api/health"
echo ""
echo "按 Ctrl+C 停止应用..."
echo "================================================"
echo ""

# 处理中断
trap "
    echo ''
    echo '停止服务...'
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
" INT

# 等待
wait
