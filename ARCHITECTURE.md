# 云端 Agent 助手工作台 - 技术架构设计文档

## 架构概览

```
┌─────────────────────────────────────────────────────────┐
│                   Web 浏览器 (3000)                      │
├─────────────────────────────────────────────────────────┤
│  React SPA Frontend                                      │
│  - SessionList 组件                                      │
│  - ChatWindow 组件                                       │
│  - API 通信层                                            │
└─────────────────────────────────────────────────────────┘
              │
              │ HTTP/REST API
              │
┌─────────────────────────────────────────────────────────┐
│          Flask Backend (5000)                            │
├─────────────────────────────────────────────────────────┤
│  API Routes:                                             │
│  - /api/health                                           │
│  - /api/sessions                                         │
│  - /api/sessions/{id}                                    │
│  - /api/sessions/{id}/messages                           │
├─────────────────────────────────────────────────────────┤
│  Session Manager                                         │
│  - 创建/加载/保存会话                                     │
│  - 消息管理                                              │
│  - 数据持久化                                            │
├─────────────────────────────────────────────────────────┤
│  Agent Engine                                            │
│  - LLM API 调用                                          │
│  - 消息处理                                              │
│  - 对话历史管理                                          │
└─────────────────────────────────────────────────────────┘
              │
              │ HTTPS
              │
┌─────────────────────────────────────────────────────────┐
│   外部 LLM API                                           │
│   https://showmevibecode.up.railway.app/api/model/v1     │
│   Model: linext-5.3-luna                                │
└─────────────────────────────────────────────────────────┘
              │
              │
┌─────────────────────────────────────────────────────────┐
│  本地文件系统                                            │
│  data/sessions/                                          │
│  ├── {session-id-1}.json                                │
│  ├── {session-id-2}.json                                │
│  └── ...                                                │
└─────────────────────────────────────────────────────────┘
```

## 核心组件详解

### 1. 前端 (React + Vite)

**主要组件**：
- `App.jsx` - 应用主容器
- `ChatWindow.jsx` - 聊天窗口和消息显示
- `SessionList.jsx` - 会话列表
- `api.js` - API 通信层

**数据流**：
```
用户输入 → 组件状态 → API 调用 → 后端处理 → 状态更新 → 界面重新渲染
```

**关键状态**：
- `sessions` - 会话列表
- `activeSessionId` - 当前选中会话 ID
- `activeSession` - 当前会话详情
- `loading` - 加载状态
- `error` - 错误信息

### 2. 后端 (Flask + Python)

#### SessionManager 类

**职责**：会话数据管理

```python
SessionManager.create_session(title, description) → Session
SessionManager.load_session(session_id) → Session | None
SessionManager.save_session(session) → None
SessionManager.list_sessions() → List[Session]
```

**数据结构**：
```python
@dataclass
class Session:
    id: str                              # UUID
    title: str                           # 会话标题
    description: str                     # 描述
    created_at: str                      # 创建时间
    updated_at: str                      # 更新时间
    status: str                          # active/completed/archived
    messages: List[Message]              # 消息列表
    metadata: Dict[str, Any]             # 元数据

@dataclass
class Message:
    id: str                              # UUID
    role: str                            # user/assistant
    content: str                         # 消息内容
    timestamp: str                       # 时间戳
    tool_calls: Optional[List[Dict]]     # 工具调用（预留）
```

#### AgentEngine 类

**职责**：AI Agent 的核心逻辑

```python
AgentEngine.call_llm(messages, temperature) → str
AgentEngine.process_message(session, user_message) → str
```

**处理流程**：
1. 构建对话历史（最后 10 条消息用于上下文）
2. 添加系统 Prompt
3. 追加用户消息
4. 调用 LLM API
5. 返回 Agent 响应

**系统 Prompt**：
```
你是一个有帮助的 AI 助手在云端工作台中。
你可以帮助用户：
1. 代码开发和调试
2. 文件处理和分析
3. 数据分析和可视化
4. 报告编写和文档

提供实用、完整的解决方案。
```

### 3. 数据持久化

**存储路径**：`data/sessions/{session-id}.json`

**会话 JSON 结构**：
```json
{
  "id": "uuid",
  "title": "会话标题",
  "description": "描述",
  "created_at": "ISO8601",
  "updated_at": "ISO8601",
  "status": "active",
  "messages": [
    {
      "id": "msg-uuid",
      "role": "user|assistant",
      "content": "消息内容",
      "timestamp": "ISO8601",
      "tool_calls": null
    }
  ],
  "metadata": {
    "task_count": 5
  }
}
```

**持久化特点**：
- 每个会话独立文件
- 自动时间戳更新
- 支持快速加载和保存
- 易于备份和迁移

## API 端点详解

### GET /api/health

**响应**：
```json
{
  "status": "healthy",
  "timestamp": "2026-11-24T02:07:51.884",
  "data_dir": "/app/data"
}
```

### GET /api/sessions

**响应**：
```json
{
  "sessions": [
    {
      "id": "uuid",
      "title": "会话标题",
      "description": "描述",
      "created_at": "ISO8601",
      "updated_at": "ISO8601",
      "status": "active",
      "message_count": 5,
      "metadata": {"task_count": 5}
    }
  ]
}
```

### POST /api/sessions

**请求**：
```json
{
  "title": "会话标题",
  "description": "描述（可选）"
}
```

**响应** (201)：
```json
{
  "id": "uuid",
  "title": "会话标题",
  "description": "描述",
  "created_at": "ISO8601",
  "status": "active",
  "message_count": 0
}
```

### POST /api/sessions/{sessionId}/messages

**请求**：
```json
{
  "message": "用户消息"
}
```

**响应** (201)：
```json
{
  "user_message": {
    "id": "msg-uuid",
    "role": "user",
    "content": "用户消息",
    "timestamp": "ISO8601"
  },
  "agent_message": {
    "id": "msg-uuid",
    "role": "assistant",
    "content": "Agent 响应",
    "timestamp": "ISO8601"
  }
}
```

## 通信流程

### 场景 1：创建会话和发送消息

```
1. 用户点击 "+ New" 按钮
   ↓
2. App 组件显示新会话表单
   ↓
3. 用户输入标题和描述，点击 Create
   ↓
4. App.handleCreateSession() 调用 api.createSession()
   ↓
5. POST /api/sessions 请求发送到后端
   ↓
6. 后端 SessionManager.create_session() 执行
   ↓
7. 返回新会话 ID
   ↓
8. 前端更新 sessions 状态，自动切换到新会话
   ↓
9. 用户开始输入消息
```

### 场景 2：发送消息和获取响应

```
1. 用户在消息框中输入并按 Enter
   ↓
2. App.handleSendMessage() 调用 api.sendMessage()
   ↓
3. POST /api/sessions/{id}/messages 请求发送
   ↓
4. 后端 SessionManager.load_session() 加载会话
   ↓
5. 添加用户消息到会话
   ↓
6. AgentEngine.process_message() 处理消息
   ↓
7. 调用 LLM API：
   - 准备消息列表
   - 设置 temperature = 0.7
   - 发送 HTTPS 请求
   - 解析响应
   ↓
8. 添加 Agent 响应到会话
   ↓
9. SessionManager.save_session() 保存会话
   ↓
10. 返回用户和 Agent 消息
   ↓
11. 前端更新 messages 列表
   ↓
12. UI 自动滚动到底部显示新消息
```

## 错误处理

### 前端错误处理

- 网络错误：显示 toast 提示
- 会话加载失败：显示错误消息
- API 超时：显示重试提示

### 后端错误处理

- 会话不存在：返回 404
- 无效的请求：返回 400
- LLM API 失败：返回带错误信息的响应
- 文件系统错误：返回 500

## 安全考虑

### 当前实现

- CORS 允许所有来源（开发环境）
- API 密钥存储在环境变量
- 无用户认证

### 生产环境建议

- 限制 CORS 源
- 配置 HTTPS/TLS
- 实现 JWT 认证
- 添加速率限制
- 输入验证和消毒
- 定期安全审计

## 性能优化建议

### 前端优化

- 虚拟列表（大量消息时）
- 消息分页加载
- 本地缓存会话列表
- 防抖/节流用户输入

### 后端优化

- 数据库替代文件存储
- 实现会话缓存
- 异步消息处理
- 连接池管理
- 日志聚合

## 扩展性

### 支持的扩展

1. **文件上传**：添加 `/api/files` 端点
2. **用户系统**：添加认证和权限
3. **实时通知**：集成 WebSocket
4. **多语言**：I18n 支持
5. **主题系统**：Dark mode 等

### 集成方式

- 保持 REST API 兼容
- 模块化后端架构
- 可插拔的前端组件

## 部署架构

### Docker 容器

```
┌────────────────────────────────────┐
│      Docker Container              │
├────────────────────────────────────┤
│  Python 3.11 + Node.js 18          │
├────────────────────────────────────┤
│  Backend (port 5000)               │
│  Frontend build (port 3000 proxy)  │
├────────────────────────────────────┤
│  Volume: ./data → /app/data        │
└────────────────────────────────────┘
```

### Docker Compose

```yaml
services:
  app:
    build: .
    ports:
      - "5000:5000"
      - "3000:3000"
    environment:
      - API_BASE_URL=...
      - API_KEY=...
    volumes:
      - ./data:/app/data
```

## 监控和日志

### 建议的监控指标

- 活跃会话数
- 消息处理延迟
- API 错误率
- 存储空间使用
- 内存占用

### 日志建议

- 请求日志（入站/出站）
- 错误堆栈跟踪
- 会话创建/删除事件
- API 调用结果

## 测试策略

### 单元测试

- SessionManager 单元测试
- AgentEngine 单元测试
- 路由处理器测试

### 集成测试

- API 端点测试
- 完整流程测试（创建→消息→更新→删除）

### E2E 测试

- 浏览器自动化测试
- 用户场景覆盖

---

**文档版本**：1.0.0
**最后更新**：2026-11-24
