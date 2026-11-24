# 🤖 Cloud Agent Assistant Workbench

一个云端 Agent 助手工作台，让用户在浏览器中创建会话、执行任务、查看进度和成果，支持多会话持久化和实时交互。

## 核心特性

- 📝 **会话管理**：创建、管理、切换多个独立会话
- 💬 **实时对话**：与 AI Agent 进行多轮对话交互
- 🔄 **任务执行**：Agent 帮助用户进行代码开发、文件处理、数据分析等工作
- 💾 **持久化存储**：会话数据本地持久化，支持关闭后继续
- 🎨 **现代化界面**：响应式 Web 界面，支持实时消息显示
- ⚡ **快速部署**：Docker 容器化部署，开箱即用

## 技术栈

- **后端**：Python + Flask
- **前端**：React + Vite
- **API 集成**：LLM API (linext-5.3-luna)
- **部署**：Docker + Docker Compose
- **数据存储**：JSON 文件存储

## 快速开始

### 前置要求

- Docker & Docker Compose
- 或 Python 3.11+ 和 Node.js 18+

### 使用 Docker（推荐）

```bash
# 克隆仓库
git clone <repository-url>
cd TalkingData_exam

# 启动应用
docker-compose up --build

# 应用将在以下地址访问
# 前端：http://localhost:3000
# 后端 API：http://localhost:5000/api
```

### 本地开发

#### 启动后端

```bash
cd backend

# 创建 Python 虚拟环境
python3 -m venv venv
source venv/bin/activate  # 或 Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 创建 .env 文件（可选，使用默认配置）
cp .env.example .env

# 启动服务
python app.py
```

后端服务将运行在 `http://localhost:5000`

#### 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端将运行在 `http://localhost:3000`

## 使用指南

### 1. 创建会话

1. 点击左侧 "🤖 Agent Workbench" 下的 "+ New" 按钮
2. 输入会话标题和描述
3. 点击 "Create" 创建会话

### 2. 开始对话

1. 在下方消息输入框中输入任务或问题
2. 按 Enter 发送消息（或 Shift+Enter 换行）
3. Agent 会处理请求并返回响应

### 3. 管理会话

- **查看会话**：在左侧列表中点击会话查看详情
- **删除会话**：点击会话右侧的 "×" 按钮
- **切换会话**：点击不同的会话在它们之间切换

### 4. 多会话使用

支持同时打开多个会话进行不同的工作：
- 一个会话进行代码开发
- 另一个会话进行数据分析
- 第三个会话进行报告整理

会话数据自动保存，关闭浏览器后仍可恢复。

## API 文档

### 健康检查

```bash
GET /api/health
```

返回服务状态和数据目录信息。

### 会话管理

#### 列表会话

```bash
GET /api/sessions
```

返回所有会话的列表。

#### 创建会话

```bash
POST /api/sessions
Content-Type: application/json

{
  "title": "会话标题",
  "description": "会话描述（可选）"
}
```

#### 获取会话详情

```bash
GET /api/sessions/{sessionId}
```

返回指定会话的完整信息（包括所有消息）。

#### 更新会话

```bash
PATCH /api/sessions/{sessionId}
Content-Type: application/json

{
  "title": "新标题",
  "description": "新描述",
  "status": "active"  // 或 "completed", "archived"
}
```

#### 删除会话

```bash
DELETE /api/sessions/{sessionId}
```

### 消息交互

#### 发送消息

```bash
POST /api/sessions/{sessionId}/messages
Content-Type: application/json

{
  "message": "用户消息内容"
}
```

返回用户消息和 Agent 响应。

## 配置说明

### 环境变量

在 `backend/.env` 中配置：

```env
# LLM API 配置
API_BASE_URL=https://showmevibecode.up.railway.app/api/model/v1
API_KEY=exam_PDOKG1XU21r1sX6gK4Dxi-f_M6kdUjt96Ve-CKfL0VQ
MODEL_NAME=linext-5.3-luna

# 服务配置
PORT=5000
DATA_DIR=./data
```

### 数据存储

所有会话数据存储在 `data/sessions/` 目录下，每个会话对应一个 JSON 文件：

```
data/
└── sessions/
    ├── {session-id-1}.json
    ├── {session-id-2}.json
    └── ...
```

会话 JSON 格式：

```json
{
  "id": "session-uuid",
  "title": "会话标题",
  "description": "会话描述",
  "created_at": "ISO8601 时间戳",
  "updated_at": "ISO8601 时间戳",
  "status": "active",
  "messages": [
    {
      "id": "message-uuid",
      "role": "user|assistant",
      "content": "消息内容",
      "timestamp": "ISO8601 时间戳"
    }
  ],
  "metadata": {
    "task_count": 5
  }
}
```

## Agent 能力说明

Agent 可以帮助用户完成以下工作：

### 代码开发
- 编写和调试代码
- 提供代码片段和示例
- 解释代码逻辑
- 性能优化建议

### 文件处理
- 分析文件内容
- 格式转换
- 数据提取

### 数据分析
- 数据分析和可视化建议
- 统计方法指导
- 趋势识别

### 文档编写
- 技术文档撰写
- 报告整理
- 内容优化

## 已知限制

1. **单用户**：当前实现为单用户使用，无用户认证和权限管理
2. **内存使用**：所有会话数据加载到内存，大规模使用时可能影响性能
3. **并发限制**：单线程处理请求，高并发时可能有性能影响
4. **文件大小**：当前不支持大文件上传和处理
5. **实时同步**：多标签页之间的会话数据不会实时同步

## 生产部署建议

在生产环境中部署时，建议：

1. **数据库升级**：使用 PostgreSQL/MongoDB 替代文件存储
2. **认证和授权**：添加用户认证机制
3. **缓存**：使用 Redis 缓存会话数据
4. **扩展性**：使用消息队列（如 RabbitMQ）处理异步任务
5. **监控**：集成日志和监控系统
6. **安全**：
   - 配置 HTTPS/TLS
   - 实现速率限制
   - 添加输入验证和防护
   - 安全存储 API 密钥

## 文件结构

```
TalkingData_exam/
├── backend/
│   ├── app.py              # Flask 应用主文件
│   ├── requirements.txt     # Python 依赖
│   ├── .env.example         # 环境变量示例
│   └── data/               # 会话数据存储
├── frontend/
│   ├── index.html          # HTML 模板
│   ├── package.json        # NPM 配置
│   ├── vite.config.js      # Vite 配置
│   └── src/
│       ├── main.jsx        # 应用入口
│       ├── App.jsx         # 主应用组件
│       ├── App.css         # 全局样式
│       ├── api.js          # API 请求封装
│       └── components/
│           ├── ChatWindow.jsx     # 聊天窗口组件
│           └── SessionList.jsx    # 会话列表组件
├── Dockerfile              # Docker 镜像定义
├── docker-compose.yml      # Docker Compose 配置
└── README.md               # 本文件
```

## 演示场景

### 场景 1：代码开发任务

1. 创建会话 "Python 工具开发"
2. 请求 Agent：创建一个爬虫工具
3. 迭代开发和优化
4. 获取完整的可运行代码

### 场景 2：数据分析任务

1. 创建会话 "数据分析"
2. 上传数据并请求分析
3. 获取分析报告和建议
4. 下载结果文档

### 场景 3：多任务并行

1. 创建会话 1：代码开发（进行中）
2. 创建会话 2：数据分析（进行中）
3. 切换会话 1，继续代码开发
4. 切换会话 2，查看分析结果
5. 两个会话数据独立且持久化

## 开发指南

### 添加新功能

1. **后端 API**：在 `backend/app.py` 中添加新路由
2. **前端组件**：在 `frontend/src/components/` 中创建新组件
3. **样式**：在 `frontend/src/App.css` 中添加样式
4. **API 客户端**：在 `frontend/src/api.js` 中添加 API 调用

### 测试

```bash
# 后端单元测试（可选）
cd backend
pytest

# 前端测试（可选）
cd frontend
npm test
```

## 故障排除

### 后端无法启动

```bash
# 检查 Python 版本
python --version

# 检查依赖安装
pip list

# 检查端口被占用
lsof -i :5000
```

### 前端无法连接到后端

```bash
# 检查后端是否运行
curl http://localhost:5000/api/health

# 检查 CORS 配置
# 确保 backend/app.py 中有 CORS(app)
```

### Docker 构建失败

```bash
# 清除缓存重新构建
docker-compose down -v
docker-compose up --build
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题或建议，请通过 GitHub Issues 联系。

---

**更新时间**：2026-11-24
**版本**：1.0.0
