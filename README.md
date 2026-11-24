## 📋 目录

- [快速开始](#快速开始)
- [功能特性](#功能特性)
- [系统需求](#系统需求)
- [安装配置](#安装配置)
- [启动方式](#启动方式)
- [使用指南](#使用指南)
- [API 文档](#api-文档)
- [常见问题](#常见问题)
- [已知限制](#已知限制)
- [项目结构](#项目结构)

---

## 🚀 快速开始

### 最快启动（Docker）

```bash
# 1. 克隆项目
git clone https://github.com/YunfeiKan/TalkingData_exam
cd TalkingData_exam

# 2. 配置环境变量
cp backend/.env.example backend/.env
# 编辑 backend/.env，填入 LLM API 的凭据

# 3. 启动应用
docker-compose up --build

# 4. 打开浏览器
访问 http://localhost:5000
```

### 本地启动

```bash
# 后端（Terminal 1）
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 app.py

# 前端（Terminal 2）
cd frontend
npm install
npm run dev
```

---

## ✨ 功能特性

### 核心功能

- **多会话管理** - 创建、编辑、删除多个独立会话
- **实时对话** - 与 AI Agent 进行多轮交互
- **LLM 集成** - 集成 `linext-5.3-luna` 大语言模型
- **数据持久化** - 会话和消息自动保存
- **一键部署** - Docker 和 Docker Compose 支持

### 应用场景

| 场景 | 说明 |
|------|------|
| 💻 代码开发 | 编写代码、调试、改进代码 |
| 📊 数据分析 | 分析数据、生成报告、数据处理 |
| 📝 文档处理 | 编写文档、翻译、文案润色 |
| 🧠 知识梳理 | 知识总结、概念解释、思维导图 |
| 🛠️ 日常工作 | 各类文本处理和工作辅助 |

---

## 🔧 系统需求

### 最低配置

- CPU: 2 核心
- 内存: 2GB RAM
- 磁盘: 2GB 空间
- 网络: 能访问 LLM API

### 推荐配置

- CPU: 4 核心
- 内存: 4GB RAM
- 磁盘: 5GB 空间

### 软件需求

- **Docker 方式**: Docker 20.10+ 和 Docker Compose 1.29+
- **本地方式**:
  - Python 3.11+
  - Node.js 18+
  - npm 9+

---

## 📦 安装配置

### 1. 克隆项目

```bash
git clone https://github.com/YunfeiKan/TalkingData_exam
cd TalkingData_exam
```

### 2. 配置环境变量

#### 获取 LLM API 凭据

从考试平台获取以下信息：
- **API 地址**: https://showmevibecode.up.railway.app/api/model/v1
- **API 密钥**: 你的考试平台凭据
- **模型名称**: linext-5.3-luna

#### 创建 .env 文件

```bash
# 复制示例文件
cp backend/.env.example backend/.env

# 编辑 backend/.env
# FLASK_ENV=development
# FLASK_DEBUG=True
# LLM_API_URL=https://showmevibecode.up.railway.app/api/model/v1
# LLM_API_KEY=your_api_key_here          # 替换为你的 API 密钥
# LLM_MODEL=linext-5.3-luna
# LLM_TEMPERATURE=0.7
# PORT=5000
# DATA_DIR=data
```

### 3. 安装依赖（本地方式）

```bash
# 后端依赖
cd backend
pip install -r requirements.txt

# 前端依赖
cd ../frontend
npm install
```

---

## 🎯 启动方式

### 方式 1：Docker Compose（推荐）

```bash
# 一键启动
docker-compose up --build

# 访问
http://localhost:3000

# 停止
docker-compose down

# 查看日志
docker-compose logs -f
```

### 方式 2：本地启动脚本

```bash
# 启动后端和前端
bash start.sh

# 访问
http://localhost:3000
```

### 方式 3：手动启动

**终端 1 - 启动后端**:
```bash
cd backend
python3 app.py
# 后端运行在 http://localhost:5000
```

**终端 2 - 启动前端**:
```bash
cd frontend
npm run dev
# 前端运行在 http://localhost:3000
```

---

## 📖 使用指南

### 基本操作

#### 1. 创建会话

1. 点击左上角 **+ New Session** 按钮
2. 输入会话标题（如：Python 爬虫开发）
3. 输入会话描述（可选）
4. 点击 **Create** 按钮
5. 自动切换到新会话

#### 2. 发送消息

1. 在底部消息框输入内容
2. 按 **Enter** 键或点击发送按钮
3. 等待 Agent 回复（通常 8-15 秒）
4. 消息自动保存

#### 3. 切换会话

- 点击左侧会话列表中的任意会话
- 自动加载该会话的所有消息

#### 4. 删除会话

- 右键点击会话，选择删除
- 或在会话上点击删除按钮

#### 5. 查看历史

- 所有消息都自动保存
- 刷新页面后消息数据恢复
- 切换会话不影响消息

### 最佳实践

**代码开发场景**:
```
1. 创建会话："Python 爬虫开发"
2. 第一条消息：清晰描述需求和要求
   例：要求使用 BeautifulSoup 和 Requests，处理异常
3. 获得代码后，提出改进意见
   例：加上日志、添加重试机制
4. 多轮迭代完善代码
```

**数据分析场景**:
```
1. 创建会话："销售数据分析"
2. 描述数据和分析目标
3. 要求生成分析方法
4. 要求生成实现代码
5. 多轮细化分析过程
```

---

## 📡 API 文档

### 基础信息

- **协议**: HTTP REST
- **基础 URL**: http://localhost:5000
- **数据格式**: JSON
- **认证**: 无（单用户场景）

### API 端点

#### 1. 健康检查

```
GET /api/health

响应:
{
  "status": "ok",
  "timestamp": "2026-11-24T10:30:00Z"
}
```

#### 2. 列表会话

```
GET /api/sessions

响应:
{
  "sessions": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Python 爬虫",
      "message_count": 5,
      "created_at": "2026-11-24T10:30:00Z"
    }
  ]
}
```

#### 3. 创建会话

```
POST /api/sessions

请求:
{
  "title": "Python 爬虫开发",
  "description": "使用 BeautifulSoup 库"
}

响应:
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Python 爬虫开发",
  "description": "使用 BeautifulSoup 库",
  "created_at": "2026-11-24T10:30:00Z"
}
```

#### 4. 获取会话详情

```
GET /api/sessions/{session_id}

响应:
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Python 爬虫开发",
  "description": "使用 BeautifulSoup 库",
  "messages": [
    {
      "role": "user",
      "content": "写一个爬虫",
      "timestamp": "2026-11-24T10:30:30Z"
    },
    {
      "role": "assistant",
      "content": "好的，这是爬虫代码...",
      "timestamp": "2026-11-24T10:30:35Z"
    }
  ],
  "created_at": "2026-11-24T10:30:00Z",
  "updated_at": "2026-11-24T10:30:35Z"
}
```

#### 5. 更新会话

```
PATCH /api/sessions/{session_id}

请求:
{
  "title": "新标题",
  "description": "新描述"
}

响应:
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "新标题",
  ...
}
```

#### 6. 删除会话

```
DELETE /api/sessions/{session_id}

响应:
{
  "success": true,
  "message": "会话已删除"
}
```

#### 7. 发送消息

```
POST /api/sessions/{session_id}/messages

请求:
{
  "message": "帮我写一个爬虫程序"
}

响应:
{
  "user_message": {
    "role": "user",
    "content": "帮我写一个爬虫程序",
    "timestamp": "2026-11-24T10:30:30Z"
  },
  "agent_message": {
    "role": "assistant",
    "content": "好的，这是爬虫代码...",
    "timestamp": "2026-11-24T10:30:35Z"
  }
}
```

### 错误响应

```
400 Bad Request:
{
  "error": "Invalid request",
  "message": "Missing required field: message"
}

404 Not Found:
{
  "error": "Session not found",
  "message": "Session with id xxx does not exist"
}

503 Service Unavailable:
{
  "error": "LLM API unavailable",
  "message": "Failed to connect to LLM API"
}
```

---

## ❓ 常见问题

### Q: 应用启动后无法访问？

**A**: 检查以下几点：
- 确保后端运行在 http://localhost:5000
- 确保前端运行在 http://localhost:3000
- 检查防火墙设置
- 查看控制台错误信息

### Q: 消息没有响应？

**A**: 可能的原因：
- 网络连接问题 - 检查互联网连接
- LLM API 配置错误 - 检查 .env 文件
- API 密钥过期 - 重新获取凭据
- API 超时 - 检查网络延迟

### Q: 数据丢失了？

**A**: 数据存储在本地 JSON 文件：
- 路径：`backend/data/sessions/{session_id}.json`
- 确保该目录未被删除
- Docker 中确保挂载了 data 卷

### Q: 如何修改 LLM 参数？

**A**: 编辑 `backend/.env` 文件：
```bash
LLM_TEMPERATURE=0.5          # 降低：更一致，升高：更创意
LLM_MODEL=linext-5.3-luna    # 更换模型
```

### Q: 支持多用户吗？

**A**: 当前版本是单用户。多用户需要添加用户认证系统。

### Q: 可以离线使用吗？

**A**: 否。需要连接到 LLM API。前端数据可本地保存，但生成内容需要网络。

---

## ⚠️ 已知限制

### 功能限制

1. **单用户** - 不支持多用户，无用户认证
2. **文件支持** - 不支持上传/下载文件
3. **流式响应** - 不支持流式输出，需要等待完整响应
4. **消息编辑** - 发送后无法编辑消息
5. **搜索功能** - 不支持跨会话搜索

### 性能限制

1. **消息数量** - 建议单个会话不超过 100 条消息
2. **上下文长度** - 最多传递 10 轮最近对话
3. **并发请求** - 单机单并发，不支持并发请求

### 数据限制

1. **存储** - JSON 文件存储，不适合大规模数据
2. **数据备份** - 需要手动备份 `backend/data` 目录
3. **数据查询** - 只支持按会话 ID 查询

### 部署限制

1. **单机部署** - 当前为单机部署，不支持分布式
2. **容器化** - Docker 中前端资源需要静态挂载
3. **持久化** - 只支持本地存储，不支持云存储

### 技术限制

1. **浏览器** - 需要现代浏览器（Chrome 60+）
2. **WebSocket** - 不支持实时通信
3. **数据库** - 使用 JSON 文件存储，扩展性有限

---

## 📁 项目结构

```
TalkingData_exam/
│
├── backend/                    # Python Flask 后端
│   ├── app.py                 # 主应用 (354 行)
│   ├── requirements.txt        # Python 依赖
│   ├── .env.example            # 环境变量示例
│   └── data/sessions/          # 会话数据存储目录
│
├── frontend/                   # React Vite 前端
│   ├── src/
│   │   ├── App.jsx            # 主组件
│   │   ├── App.css            # 样式表
│   │   ├── api.js             # API 客户端
│   │   ├── components/        # React 组件
│   │   └── main.jsx           # 应用入口
│   ├── index.html             # HTML 模板
│   ├── vite.config.js         # Vite 配置
│   └── package.json           # NPM 配置
│
├── Dockerfile                  # Docker 镜像配置
├── docker-compose.yml          # Docker Compose 配置
├── start.sh                    # 启动脚本
├── README.md                   # 此文件
└── DESIGN.md                   # 完整设计文档

# 运行后生成
backend/data/sessions/         # 会话数据（JSON 文件）
frontend/dist/                 # 前端构建产物
```

---

## 🔄 工作流程

```
用户操作 → React UI → HTTP API → Python 后端
                                      ↓
                              SessionManager (会话管理)
                              AgentEngine (LLM 调用)
                                      ↓
                           LLM API (linext-5.3-luna)
                                      ↓
                              JSON 文件 (数据保存)
                                      ↓
                           响应回复 → 前端更新 → UI 显示
```

---

## 📊 技术栈

| 层 | 技术 | 版本 |
|----|------|------|
| 前端 | React | 18+ |
| 前端构建 | Vite | 5+ |
| 后端 | Python Flask | 3.0+ |
| 部署 | Docker | 20.10+ |
| LLM 集成 | HTTP REST | - |
| 数据存储 | JSON | - |

---

## 📝 许可证

MIT License

---

## 🙋 获取帮助

- **完整设计文档**: 查看 [DESIGN.md](DESIGN.md)
- **问题报告**: GitHub Issues
- **代码查看**: GitHub 仓库源码

---

**版本**: 1.0  
**最后更新**: 2026-11-24  
**状态**: 生产就绪

