# 快速启动和演示指南

## 一、应用启动

### 前置条件
- Docker 和 Docker Compose 已安装
- 端口 5000 未被占用
- 网络连接正常（需要调用 Claude API）

### 启动命令

```bash
cd /workspaces/TalkingData_exam
docker-compose up --build
```

### 预期输出
```
[+] Building 15.2s (19/19) FINISHED
[+] up 2/2
✔ Image talkingdata_exam-app Built
✔ Container agent-workbench Recreated
Attaching to agent-workbench

Application started on http://localhost:5000
```

### 访问应用
打开浏览器访问：**http://localhost:5000**

---

## 二、演示流程（3-5 分钟）

### 步骤 1：查看会话列表（1 分钟）

**应该看到：**
- 左侧边栏显示 2 个已有会话
- 会话 1：「Python 爬虫工具 - 增强版」
- 会话 2：「销售数据分析」
- 右上角「新建会话」按钮

**说明：**
这两个会话是演示数据，包含完整的对话历史和工作记录。

---

### 步骤 2：查看代码开发会话（1-2 分钟）

**点击：** 「Python 爬虫工具 - 增强版」

**应该看到：**
- 聊天区域显示 4 条消息
- 消息 1：用户请求「帮我写一个 Python 爬虫」
- 消息 2：助手回复完整代码框架
- 消息 3：用户追问「能加上错误处理吗？」
- 消息 4：助手提供增强版本代码

**验证项：**
- [x] 对话内容清晰完整
- [x] 消息顺序正确（从旧到新）
- [x] 时间戳显示正确
- [x] 用户/助手身份区分明显

**说明：**
这个演示展示了应用处理**编程任务**的能力，包括多轮对话和代码迭代。

---

### 步骤 3：查看日常工作会话（1-2 分钟）

**点击：** 「销售数据分析」

**应该看到：**
- 聊天区域显示 2 条消息
- 消息 1：用户上传数据「我有过去 6 个月的销售数据，请分析增长趋势」
- 消息 2：助手回复数据分析方法和要求

**验证项：**
- [x] 对话内容清晰完整
- [x] 消息顺序正确
- [x] 时间戳显示正确
- [x] 显示日期和具体时间

**说明：**
这个演示展示了应用处理**日常工作任务**的能力，包括数据分析、报告生成等。

---

### 步骤 4：测试会话切换和数据持久化（1 分钟）

**执行操作：**
1. 在「销售数据分析」和「Python 爬虫工具」间快速切换
2. 按 F5 刷新页面
3. 再次点击任意会话

**应该看到：**
- 切换时对话内容立即更新
- 刷新后会话列表保留
- 刷新后对话历史保留，无数据丢失

**验证项：**
- [x] 会话切换流畅
- [x] 数据加载迅速
- [x] 数据持久化有效

**说明：**
这验证了应用的核心功能：**多会话管理**和**数据持久化**。

---

## 三、创建新会话（可选演示）

### 创建新会话
**点击：** 右上角「新建会话」按钮

**输入：**
- 标题：「示例任务」
- 描述：「演示新会话创建」

**点击：** 「创建」

**应该看到：**
- 新会话出现在会话列表
- 自动切换到新会话
- 聊天区域为空，等待输入

### 进行对话（演示）
在聊天框输入：
```
帮我用 Python 写一个简单的计算器程序
```

**应该看到：**
- 消息即时显示
- 时间戳自动生成
- 助手开始生成回复

---

## 四、关键功能演示总结

| 功能 | 演示位置 | 预期行为 |
|-----|--------|--------|
| 多会话管理 | 左侧会话列表 | 显示 2 个演示会话 |
| 对话显示 | 聊天区域 | 完整的消息历史 |
| 切换会话 | 点击会话名 | 内容立即更新 |
| 数据持久化 | 刷新页面 | 数据保留 |
| 新建会话 | 右上角按钮 | 创建新会话 |
| 实时对话 | 聊天输入框 | 消息即时显示 |
| 消息时戳 | 每条消息旁 | 显示日期和时间 |

---

## 五、疑难排查

### 问题 1：应用无法启动

**症状：** Docker 错误或连接失败

**解决：**
```bash
# 检查依赖
docker-compose down
docker-compose build --no-cache
docker-compose up

# 或查看日志
docker-compose logs -f
```

### 问题 2：端口已被占用

**症状：** `address already in use 0.0.0.0:5000`

**解决：**
```bash
# 查看占用进程
lsof -i :5000

# 释放端口
kill -9 <PID>

# 或修改 docker-compose.yml 中的端口
# 将 "5000:5000" 改为 "5001:5000"
```

### 问题 3：会话数据未显示

**症状：** 应用加载但没有会话

**解决：**
```bash
# 检查数据文件
ls -la backend/data/sessions/

# 验证 JSON 有效性
python3 -m json.tool backend/data/sessions/*.json

# 重启容器
docker-compose restart
```

### 问题 4：API 连接失败

**症状：** 对话无响应或报错

**解决：**
```bash
# 检查环境变量
echo $API_KEY
echo $API_URL

# 检查网络连接
curl https://showmevibecode.up.railway.app/api/model/v1

# 查看应用日志
docker-compose logs app
```

---

## 六、应用配置

### 环境变量（.env）
```
API_URL=https://showmevibecode.up.railway.app/api/model/v1
API_KEY=exam_PDOKG1XU21r1sX6gK4Dxi-f_M6kdUjt96Ve-CKfL0VQ
MODEL=linext-5.3-luna
PORT=5000
FLASK_ENV=production
```

### 数据存储位置
```
backend/data/
├── sessions/          # 会话数据
│   ├── [session_id_1].json
│   └── [session_id_2].json
└── uploads/          # 用户上传的文件
```

### 日志位置
```
backend/logs/
└── app.log           # 应用日志
```

---

## 七、常见操作

### 保存演示会话
```bash
# 备份会话数据
cp -r backend/data/sessions demo_sessions_backup
tar -czf demo_sessions_backup.tar.gz demo_sessions_backup/
```

### 重置应用（清除所有会话）
```bash
# 警告：此操作不可逆
rm -rf backend/data/sessions/*
docker-compose restart
```

### 查看会话详情
```bash
# 格式化显示 JSON
python3 -m json.tool backend/data/sessions/[session_id].json

# 统计消息
grep -c '"role":' backend/data/sessions/[session_id].json
```

---

## 八、演示要点

### 核心价值
✓ **多会话独立管理** - 同时处理多个工作  
✓ **完整对话历史** - 保留所有交互记录  
✓ **数据持久化** - 刷新不丢失数据  
✓ **多场景适应** - 编程、分析、文案等  
✓ **实时交互** - 消息即时显示  

### 应用场景
1. **代码开发** - 获取编程帮助和代码审查
2. **数据分析** - 处理数据文件和生成报告
3. **文档整理** - 整理材料和撰写文案
4. **知识咨询** - 获取技术和业务建议

---

## 九、后续工作

### 用户可以继续的操作
- [ ] 在爬虫会话中继续优化代码
- [ ] 在数据分析会话中上传实际数据
- [ ] 创建新会话处理其他任务
- [ ] 下载生成的代码和报告
- [ ] 切换会话进行不同工作

### 推荐演示时间
- **短版本（3 分钟）：** 步骤 1-3
- **完整版本（5 分钟）：** 步骤 1-4 + 新建会话
- **深度演示（10 分钟）：** 完整版本 + 创建新会话并交互

---

**应用已准备好用于演示。按照上述步骤进行，所有功能都能清晰展示。**
