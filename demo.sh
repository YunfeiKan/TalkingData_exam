#!/bin/bash

# 云端 Agent 助手工作台 - 演示脚本

API_BASE="http://localhost:5000/api"

echo "🤖 云端 Agent 助手工作台 - 演示脚本"
echo "================================================"
echo ""

# 1. 健康检查
echo "1️⃣ 健康检查"
echo "   GET /api/health"
response=$(curl -s $API_BASE/health)
echo "   响应: $response"
echo ""

# 2. 创建会话 1 - 代码开发
echo "2️⃣ 创建会话 1: 代码开发"
echo "   POST /api/sessions"
session1=$(curl -s -X POST $API_BASE/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python 工具开发",
    "description": "开发一个数据处理工具"
  }')
SESSION1_ID=$(echo $session1 | grep -o '"id":"[^"]*' | head -1 | cut -d'"' -f4)
echo "   创建成功! 会话 ID: $SESSION1_ID"
echo ""

# 3. 创建会话 2 - 数据分析
echo "3️⃣ 创建会话 2: 数据分析"
echo "   POST /api/sessions"
session2=$(curl -s -X POST $API_BASE/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "title": "数据分析报告",
    "description": "分析销售数据并生成报告"
  }')
SESSION2_ID=$(echo $session2 | grep -o '"id":"[^"]*' | head -1 | cut -d'"' -f4)
echo "   创建成功! 会话 ID: $SESSION2_ID"
echo ""

# 4. 列表会话
echo "4️⃣ 列表会话"
echo "   GET /api/sessions"
curl -s $API_BASE/sessions | python3 -m json.tool
echo ""

# 5. 发送消息到会话 1
echo "5️⃣ 发送消息到会话 1 (代码开发)"
echo "   用户: 帮我写一个 Python 爬虫用于获取网页数据"
message1=$(curl -s -X POST $API_BASE/sessions/$SESSION1_ID/messages \
  -H "Content-Type: application/json" \
  -d '{
    "message": "帮我写一个 Python 爬虫用于获取网页数据"
  }')
echo "   Agent 响应:"
echo $message1 | python3 -c "
import sys, json
data = json.load(sys.stdin)
print('   ' + data['agent_message']['content'][:200] + '...')
"
echo ""

# 6. 发送消息到会话 2
echo "6️⃣ 发送消息到会话 2 (数据分析)"
echo "   用户: 我有一份 CSV 文件包含过去一年的销售数据，请帮我分析趋势"
message2=$(curl -s -X POST $API_BASE/sessions/$SESSION2_ID/messages \
  -H "Content-Type: application/json" \
  -d '{
    "message": "我有一份 CSV 文件包含过去一年的销售数据，请帮我分析趋势"
  }')
echo "   Agent 响应:"
echo $message2 | python3 -c "
import sys, json
data = json.load(sys.stdin)
print('   ' + data['agent_message']['content'][:200] + '...')
"
echo ""

# 7. 获取会话 1 详情
echo "7️⃣ 获取会话 1 详情"
echo "   GET /api/sessions/$SESSION1_ID"
curl -s $API_BASE/sessions/$SESSION1_ID | python3 -m json.tool | head -20
echo "   ..."
echo ""

# 8. 更新会话 1
echo "8️⃣ 更新会话 1 标题"
echo "   PATCH /api/sessions/$SESSION1_ID"
curl -s -X PATCH $API_BASE/sessions/$SESSION1_ID \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python 爬虫工具开发 (已更新)"
  }' | python3 -m json.tool
echo ""

# 9. 继续对话
echo "9️⃣ 继续会话 1 中的对话"
echo "   用户: 能帮我加上错误处理吗?"
message3=$(curl -s -X POST $API_BASE/sessions/$SESSION1_ID/messages \
  -H "Content-Type: application/json" \
  -d '{
    "message": "能帮我加上错误处理吗?"
  }')
echo "   Agent 响应:"
echo $message3 | python3 -c "
import sys, json
data = json.load(sys.stdin)
print('   ' + data['agent_message']['content'][:200] + '...')
"
echo ""

# 10. 最终列表
echo "🔟 最终会话列表"
echo "   GET /api/sessions"
curl -s $API_BASE/sessions | python3 -c "
import sys, json
data = json.load(sys.stdin)
for session in data['sessions']:
    print(f\"   - {session['title']} ({session['message_count']} 条消息)\")
"
echo ""

echo "================================================"
echo "✅ 演示完成!"
echo ""
echo "📱 访问 http://localhost:3000 查看完整 UI"
echo "================================================"
