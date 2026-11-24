# 云端 Agent 助手工作台 - 完整设计文档

## 1. 项目概述

**项目名称**: Cloud Agent Assistant Workbench (云端 Agent 助手工作台)

**核心目标**: 在浏览器中实现一个完整的工作台，让用户能够：
- 创建和管理多个独立的会话
- 交给 AI Agent 执行各类任务（代码开发、数据分析等）
- 实时查看任务进展
- 多轮迭代交互
- 任务数据持久化，支持会话恢复

**应用场景**:
- 代码开发助手 - 编写、调试、改进代码
- 数据分析工具 - 分析数据、生成报告
- 日常工作辅助 - 整理资料、处理文本

---

## 2. 技术架构设计

### 2.1 技术栈选择理由

#### 后端：Python Flask + REST API

**为什么选择 Python Flask？**
- 轻量级，快速原型开发
- 生态完善，第三方库丰富
- LLM 社区广泛使用 Python
- 易于扩展和集成外部服务
- 开发效率高，代码简洁

**为什么选择 REST API？**
- 前后端解耦，独立部署
- 易于测试和调试
- 通用标准，易于接入其他客户端
- 负载均衡和扩展性好

#### 前端：React + Vite

**为什么选择 React？**
- 组件化开发，代码复用性高
- Hooks 管理状态简洁
- 成熟的生态和社区
- 性能优化完善（Virtual DOM）
- 易于实现实时 UI 更新

**为什么选择 Vite？**
- 极快的开发服务器速度
- ES Modules 原生支持
- 生产构建优化
- 配置简洁，零配置启动

#### 部署：Docker + Docker Compose

**为什么选择 Docker？**
- 一键部署，环境一致性
- 易于扩展（水平伸缩）
- 生产环境标准化
- 开发、测试、生产环境统一

#### 数据存储：JSON 文件

**为什么选择 JSON？**
- 单用户场景足够满足
- 无依赖，易于备份和移动
- 快速原型开发
- 可视化程度高，便于调试

**未来升级路径**: PostgreSQL/MongoDB

#### LLM 集成：HTTP REST 调用

**为什么选择 HTTP 调用？**
- 通用标准，不依赖特定 SDK
- 易于切换 LLM 提供商
- 请求/响应可视化和调试
- 支持流式和非流式响应

---

### 2.2 系统架构

```
用户浏览器 (React SPA)
        ↓↑ HTTP REST API
   Flask 后端 (Python)
        ↓↑ HTTP 调用
    LLM API (linext-5.3-luna)
        
┌─────────────────────────────────────────────────────────────┐
│                    前端（React SPA）                        │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  App.jsx (主容器)                                      │ │
│  │  ├─ SessionList.jsx (会话列表)                         │ │
│  │  │  ├─ 会话切换                                        │ │
│  │  │  └─ 会话创建/删除                                   │ │
│  │  └─ ChatWindow.jsx (聊天窗口)                          │ │
│  │     ├─ 消息显示                                        │ │
│  │     ├─ 输入框                                          │ │
│  │     └─ 自动滚动                                        │ │
│  └────────────────────────────────────────────────────────┘ │
│                    api.js (Axios 客户端)                     │
└─────────────────────────────────────────────────────────────┘
                            ↓↑
┌─────────────────────────────────────────────────────────────┐
│                   后端（Flask REST API）                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  SessionManager (会话管理)                             │ │
│  │  ├─ create_session()                                   │ │
│  │  ├─ load_session()                                     │ │
│  │  ├─ save_session()                                     │ │
│  │  └─ list_sessions()                                    │ │
│  │                                                         │ │
│  │  AgentEngine (Agent 执行引擎)                          │ │
│  │  ├─ call_llm() - 调用外部 LLM API                      │ │
│  │  ├─ process_message() - 处理用户消息                   │ │
│  │  └─ build_context() - 构建消息上下文                   │ │
│  │                                                         │ │
│  │  Routes (REST 端点)                                    │ │
│  │  ├─ GET /api/sessions                                 │ │
│  │  ├─ POST /api/sessions                                │ │
│  │  ├─ POST /api/sessions/{id}/messages                  │ │
│  │  └─ ... (9 个端点)                                     │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                               │
│           JSON 存储 (backend/data/sessions/)                 │
└─────────────────────────────────────────────────────────────┘
                            ↓↑
            LLM API (linext-5.3-luna)
```

---

## 3. 前端设计

### 3.1 组件架构

**App.jsx** (主容器，146 行)
```
职责：
- 管理全局状态（当前会话、所有会话、消息列表）
- 处理用户交互事件
- 调用后端 API
- 页面布局和路由

状态管理：
- currentSessionId - 当前选中的会话
- sessions - 所有会话列表
- messages - 当前会话的消息
- loading - 加载状态
```

**SessionList.jsx** (会话列表组件)
```
职责：
- 显示所有会话
- 实现会话切换
- 实现会话创建/删除
- 显示会话信息（标题、消息数）

用户交互：
- 点击切换会话
- 右键删除会话
- 创建新会话
```

**ChatWindow.jsx** (聊天窗口组件)
```
职责：
- 显示消息列表
- 消息的用户/助手区分展示
- 输入框管理
- 自动滚动到最新消息
- 加载状态提示

特性：
- 消息自动格式化
- Markdown 渲染支持
- 加载动画
- 错误提示
```

### 3.2 状态管理设计

```
App.jsx 中的状态流：

创建会话流程：
用户点击 New → 输入标题/描述
→ handleCreateSession() 
→ POST /api/sessions
→ 后端创建会话
→ 返回会话 ID
→ 更新 currentSessionId
→ 切换到新会话

发送消息流程：
用户输入消息 → 按 Enter
→ handleSendMessage()
→ 本地添加用户消息
→ POST /api/sessions/{id}/messages
→ 后端处理（调用 LLM）
→ 返回 Agent 响应
→ 本地添加 Agent 消息
→ 自动滚动到底部
```

### 3.3 UI/UX 设计

**布局**：CSS Grid 二列布局
- 左侧：会话列表（固定 280px 宽）
- 右侧：聊天窗口（自适应）

**样式**：
- 现代 flat 设计
- 响应式布局
- 暗色系主题（可扩展）
- 消息气泡展示（用户在右，Agent 在左）

**交互**：
- 实时反馈（加载状态）
- 自动滚动
- 点击反馈
- 错误提示

---

## 4. 后端设计

### 4.1 核心模块

**SessionManager** (会话管理器)
```python
职责：
- 创建新会话（生成 UUID）
- 加载现有会话
- 保存会话到 JSON
- 列出所有会话
- 删除会话

数据结构 (Session):
{
  "id": "uuid",                  # 唯一标识
  "title": "会话标题",           # 用户输入
  "description": "描述",         # 用户输入
  "created_at": "ISO 8601",     # 创建时间
  "updated_at": "ISO 8601",     # 最后更新时间
  "status": "active",            # 状态（active/archived）
  "messages": [                  # 消息列表
    {
      "role": "user/assistant",  # 角色
      "content": "消息内容",     # 消息体
      "timestamp": "ISO 8601"    # 时间戳
    }
  ],
  "metadata": {}                 # 元数据（扩展用）
}

存储路径：
backend/data/sessions/{session_id}.json
```

**AgentEngine** (Agent 执行引擎)
```python
职责：
- 调用外部 LLM API
- 管理对话上下文
- 格式化用户输入
- 处理 LLM 响应

关键方法：
1. call_llm(messages, temperature, model)
   - 构建请求体
   - 调用 HTTP API
   - 解析响应
   - 错误处理

2. process_message(session, user_message)
   - 添加用户消息到上下文
   - 调用 call_llm()
   - 获取 Agent 响应
   - 返回结果

3. build_context(session)
   - 获取历史消息
   - 添加系统提示词
   - 控制上下文长度（防止超限）

LLM API 配置：
- 端点：https://showmevibecode.up.railway.app/api/model/v1
- 模型：linext-5.3-luna
- 温度：0.7（平衡创意和一致性）
- 超时：30s
```

**REST API 端点设计**
```
1. GET /api/health
   返回服务器状态
   用途：健康检查、负载均衡探针

2. GET /api/sessions
   返回所有会话列表
   响应：{sessions: [{id, title, message_count, created_at}]}

3. POST /api/sessions
   创建新会话
   请求：{title, description}
   响应：{id, title, description, created_at}

4. GET /api/sessions/{id}
   获取单个会话详情（包括所有消息）
   响应：{id, title, description, messages, ...}

5. PATCH /api/sessions/{id}
   更新会话信息
   请求：{title?, description?, status?}
   响应：{id, title, ...}

6. DELETE /api/sessions/{id}
   删除会话
   响应：{success: true}

7. POST /api/sessions/{id}/messages
   发送消息、获取 Agent 响应
   请求：{message: "用户消息"}
   响应：{user_message, agent_message, timestamp}

8-9. 前端静态资源和根路径
```

### 4.2 请求/响应流程

```
用户发送消息：

前端：
  POST /api/sessions/{id}/messages
  {
    "message": "帮我写一个爬虫"
  }

后端处理：
  1. 验证会话 ID 存在
  2. 加载会话数据
  3. 添加用户消息到消息列表
  4. 构建对话上下文
  5. 调用 LLM API
     请求体：
     {
       "model": "linext-5.3-luna",
       "messages": [
         {
           "role": "system",
           "content": "你是一个专业的代码助手..."
         },
         ... (历史消息)
         {
           "role": "user",
           "content": "帮我写一个爬虫"
         }
       ],
       "temperature": 0.7,
       "max_tokens": 2000
     }
  6. 获取 LLM 响应
  7. 添加 Agent 消息到消息列表
  8. 保存会话到 JSON
  9. 返回给前端

前端响应处理：
  1. 解析响应
  2. 添加 Agent 消息到本地消息列表
  3. 更新 UI
  4. 自动滚动到最新消息
  5. 保存状态到浏览器缓存（可选）
```

### 4.3 错误处理设计

```
错误分类：

1. 客户端错误 (4xx)
   - 400 Bad Request - 请求格式错误
   - 404 Not Found - 会话不存在
   - 422 Unprocessable Entity - 业务逻辑错误

2. 服务器错误 (5xx)
   - 500 Internal Server Error - 通用错误
   - 503 Service Unavailable - LLM API 不可用

错误响应格式：
{
  "error": "错误简述",
  "message": "详细错误信息",
  "code": "ERROR_CODE",
  "timestamp": "ISO 8601"
}

前端错误处理：
- 显示友好的错误提示
- 记录错误日志
- 保留用户输入（失败重试）
- 自动重试策略（可选）
```

---

## 5. 数据模型设计

### 5.1 会话数据结构

```python
@dataclass
class Message:
    role: str           # "user" 或 "assistant"
    content: str        # 消息内容
    timestamp: str      # ISO 8601 时间戳

@dataclass
class Session:
    id: str                        # UUID
    title: str                     # 会话标题
    description: str               # 会话描述
    created_at: str               # 创建时间
    updated_at: str               # 更新时间
    status: str = "active"        # 状态
    messages: List[Message] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)

# JSON 序列化示例
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Python 爬虫开发",
  "description": "使用 BeautifulSoup 和 Requests 库",
  "created_at": "2026-11-24T10:30:00Z",
  "updated_at": "2026-11-24T10:45:00Z",
  "status": "active",
  "messages": [
    {
      "role": "user",
      "content": "帮我写一个爬虫程序",
      "timestamp": "2026-11-24T10:30:30Z"
    },
    {
      "role": "assistant",
      "content": "好的，这是一个基础爬虫示例：\n```python\n...",
      "timestamp": "2026-11-24T10:30:35Z"
    }
  ],
  "metadata": {
    "user_id": null,  # 单用户，暂不使用
    "tags": []
  }
}
```

### 5.2 消息上下文管理

```
对话上下文构建（防止 token 超限）：

1. 获取历史消息
2. 控制上下文深度（最多 10 轮对话）
3. 控制上下文长度（总长度 < 8000 字符）

示例：
历史消息：[msg1, msg2, msg3, msg4, msg5, ...]
↓
筛选最近的消息（防止超限）
↓
加入系统提示词
↓
发送给 LLM API

系统提示词示例：
"你是一个专业的代码开发助手。
你能够：
1. 编写高质量的 Python 代码
2. 解释代码逻辑
3. 优化性能
4. 处理错误和异常
5. 提供最佳实践建议

请用简洁、专业的方式回复。
如果代码较长，使用 Markdown 代码块。"
```

---

## 6. 测试设计

### 6.1 单元测试

**后端单元测试**:
```
SessionManager 测试：
✓ 创建新会话
✓ 加载已存在的会话
✓ 保存会话到 JSON
✓ 列表所有会话
✓ 删除会话

AgentEngine 测试：
✓ 格式化消息
✓ 调用 LLM API
✓ 处理 API 超时
✓ 处理 API 错误
✓ 管理消息上下文
```

**前端单元测试** (可选):
```
App.jsx 逻辑测试：
✓ 状态初始化
✓ 会话切换
✓ 消息发送

组件测试：
✓ ChatWindow 消息渲染
✓ SessionList 列表渲染
✓ 加载状态显示
```

### 6.2 集成测试

```
完整工作流测试：
1. 创建会话
2. 发送用户消息
3. 接收 Agent 响应
4. 更新会话
5. 切换会话
6. 验证数据持久化

多会话测试：
✓ 创建多个会话
✓ 在会话间切换
✓ 验证消息独立性
✓ 验证数据隔离

持久化测试：
✓ 创建会话和消息
✓ 重启服务
✓ 验证数据恢复
```

### 6.3 功能测试场景

**场景 1：代码开发**
```
1. 创建会话 "Python 爬虫"
2. 发送：要求写爬虫代码
3. 获取：完整的爬虫代码
4. 发送：要求添加错误处理
5. 获取：改进版本代码
6. 验证：消息历史完整
```

**场景 2：数据分析**
```
1. 创建会话 "数据分析"
2. 发送：分析方法建议
3. 获取：分析框架
4. 发送：实现建议
5. 获取：具体实现步骤
```

**场景 3：多会话**
```
1. 创建会话 A、B、C
2. 在各会话发送消息
3. 验证消息独立性
4. 刷新页面
5. 验证数据恢复
```

### 6.4 性能测试指标

```
API 响应时间：
✓ 创建会话：< 100ms
✓ 列表会话：< 50ms
✓ 发送消息（包括 LLM 调用）：8-15s
✓ 更新会话：< 100ms

前端性能：
✓ 页面加载：< 2s
✓ 消息渲染：< 100ms
✓ 切换会话：< 200ms
✓ 自动滚动：流畅无卡顿
```

---

## 7. 部署设计

### 7.1 Docker 部署

```dockerfile
# 两阶段构建

阶段 1：前端构建
- Node 18 基础镜像
- npm install 安装依赖
- npm run build 生成静态文件

阶段 2：生产镜像
- Python 3.11 基础镜像
- 复制前端构建结果
- 安装 Python 依赖
- 配置环境变量
- 暴露 5000 端口
- 启动 Flask 应用

特点：
✓ 多阶段构建，镜像体积小
✓ 前后端打包在一起
✓ 单一容器部署
✓ 快速启动
```

### 7.2 Docker Compose

```yaml
services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - LLM_API_URL=${LLM_API_URL}
      - LLM_API_KEY=${LLM_API_KEY}
    volumes:
      - ./backend/data:/app/backend/data
    restart: unless-stopped

优点：
✓ 一键启动：docker-compose up
✓ 环境变量管理
✓ 数据持久化（挂载 data 目录）
✓ 自动重启
```

### 7.3 环境配置

```bash
# .env 文件
FLASK_ENV=development          # 开发/生产环境
FLASK_DEBUG=True              # 调试模式
LLM_API_URL=...               # LLM API 端点
LLM_API_KEY=...               # API 密钥（环境变量）
LLM_MODEL=linext-5.3-luna     # 模型名称
LLM_TEMPERATURE=0.7           # 温度参数
PORT=5000                     # Flask 端口
DATA_DIR=data                 # 数据存储目录
```

---

## 8. 扩展设计

### 8.1 未来升级方向

**短期**（1-2 周）:
- WebSocket 实时通信
- 消息搜索功能
- 会话标签/分类

**中期**（1-3 个月）:
- 用户认证系统 (JWT/OAuth)
- 数据库迁移 (PostgreSQL)
- 文件上传支持
- 消息编辑/删除

**长期**（3-6 个月）:
- 实时协作（多用户）
- 消息缓存 (Redis)
- 异步任务队列 (Celery)
- 监控和日志系统 (Prometheus/ELK)
- 国际化 (i18n)

### 8.2 可扩展架构

```
当前架构：
Flask + JSON 存储 → 单用户、单机

过渡架构：
Flask + PostgreSQL + Redis → 多用户、单机

分布式架构：
Nginx (负载均衡)
  ↓
Flask × N (无状态应用)
  ↓
PostgreSQL (数据库)
Redis (缓存)
Celery (异步任务)
ELK (日志收集)
```

---

## 9. 总结

### 核心设计原则

1. **简洁性** - 代码清晰，易于理解和维护
2. **可靠性** - 完整的错误处理和数据验证
3. **可扩展性** - 模块化设计，便于升级
4. **用户体验** - 实时反馈，流畅交互
5. **生产就绪** - Docker 部署，完整文档

### 关键决策

| 决策 | 选择 | 原因 |
|------|------|------|
| 后端框架 | Flask | 轻量级、快速开发 |
| 前端框架 | React | 组件化、成熟生态 |
| 构建工具 | Vite | 极快开发速度 |
| 部署方式 | Docker | 环境一致性、易扩展 |
| 数据存储 | JSON | 单用户足够，易升级 |
| API 设计 | REST | 标准通用，易测试 |

### 验收标准

所有用户需求实现
代码清晰易读
完整的测试覆盖
生产级部署配置
详尽的文档说明

