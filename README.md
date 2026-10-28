# IOOI 情绪蛋

面向青少年的情绪陪伴硬件与数据平台。硬件端完成情绪感知与多模态反馈，云端负责数据留存、趋势分析与社区互动，用户通过 Web 端回顾自己的情绪变化。

> 本项目为竞赛作品，曾获 2024 中美青年创客大赛中美赛区二等奖、厦门赛区一等奖，并参加 2024 海峡两岸信息创新创业大赛。

---

## 系统架构

```
┌─────────────────┐        ┌──────────────────┐        ┌─────────────────┐
│  端 · 情绪蛋硬件  │        │   云 · Go 后端    │        │  前端 · 用户侧   │
│                 │        │                  │        │                 │
│  录音采集        │  HTTP  │  设备接入         │  HTTP  │  情绪看板        │
│  情绪识别        │ ─────► │  账号体系         │ ◄───── │  社区广场        │
│  生成建议        │  上报  │  互动存储         │  查询  │  个人主页        │
│  语音与表情反馈   │        │  趋势聚合         │        │  登录注册        │
└─────────────────┘        └──────────────────┘        └─────────────────┘
       Python                 Gin + GORM                    HTML + JS
                              PostgreSQL
```

三层的职责边界：

- **端**：感知与反馈闭环。采集语音、识别情绪、生成陪伴建议、合成语音并播放对应情绪的表情动画。算力与网络受限，因此交互必须低延迟，网络异常时需本地缓存。
- **云**：数据中枢。承接设备上报、管理账号与设备归属、按时间维度聚合情绪趋势、维护社区内容。
- **前端**：数据呈现。用户与家长查看历史趋势和社区内容。

---

## 技术栈

| 层次 | 技术 | 选型理由 |
|------|------|----------|
| 后端语言 | Go 1.23 | 静态编译、单二进制部署，适合资源受限的边缘场景 |
| Web 框架 | Gin | 路由与中间件模型清晰，生态成熟 |
| ORM | GORM | 模型定义即表结构，开发期迭代快 |
| 数据库 | PostgreSQL | 需要窗口函数与 `mode()` 聚合来完成情绪众数统计 |
| 认证 | JWT (HS256) | 无状态，设备与浏览器端可共用一套鉴权模型 |
| 密码存储 | bcrypt | 自带盐值与计算成本，抗彩虹表与暴力破解 |
| 前端 | 原生 HTML + ES Module + Tailwind | 页面规模小，引入构建链的收益低于维护成本 |
| 部署 | Docker Compose | 一条命令拉起数据库与应用，降低他人复现成本 |

---

## 快速开始

### 前置要求

- Docker Desktop（推荐，无需本地安装 PostgreSQL）
- 或：Go 1.23+ 与 PostgreSQL 14+

### 方式一：容器启动（推荐）

```bash
# 1. 准备配置
cp .env.example .env

# 2. 生成 JWT 密钥并填入 .env 的 JWT_SECRET
openssl rand -base64 32

# 3. 启动数据库与应用
docker compose up -d --build

# 4. 确认服务已就绪
curl http://localhost:8080/api/emotion-years
```

停止服务：`docker compose down`
连同数据一起清除：`docker compose down -v`

### 方式二：本地运行后端

```bash
cp .env.example emotion_database/.env
# 确认 .env 中 DB_HOST 指向本地数据库，并填写 JWT_SECRET

cd emotion_database
go mod download
go run .
```

服务默认监听 `http://localhost:8080`。

前端为静态页面，用任意静态服务器打开即可：

```bash
cd emotional_egg/public
python -m http.server 5500
```

> 前端 `src/js/config.js` 中的 `baseURL` 目前指向 `http://localhost:8080`，部署时需同步修改。

---

## 接口一览

### 公开接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/user/register` | 用户注册 |
| POST | `/user/login` | 用户登录，返回 JWT |
| POST | `/api/emotion/upload` | 设备上报一次情绪互动记录 |
| GET | `/api/emotion/all` | 查询指定用户的全部情绪记录 |
| GET | `/api/emotion-years` | 查询该用户有记录的年份 |
| GET | `/api/emotions/dominant` | 按 年/月/周/日 维度返回情绪众数趋势 |

### 需鉴权接口

请求头需携带 `Authorization: Bearer <token>`。

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/log/user/profile` | 获取当前用户资料与互动记录数 |
| PUT | `/log/user/profile` | 修改签名与头像 |
| GET | `/log/user/lastInteraction` | 获取最近一次互动，用于看板顶部展示 |
| GET | `/log/community/posts` | 获取社区帖子列表 |
| POST | `/log/community/post` | 发布社区帖子（当前由设备端调用） |

---

## 目录结构

```
.
├── emotion_database/          # Go 后端
│   ├── config/                # 配置加载，统一读取环境变量
│   ├── controller/            # HTTP 处理器
│   ├── database/              # 数据库连接与自动迁移
│   ├── middleware/            # JWT 鉴权中间件
│   ├── model/                 # 数据模型定义
│   ├── router/                # 路由注册与 CORS
│   ├── Dockerfile
│   └── main.go                # 程序入口
├── emotional_egg/             # 前端静态资源
│   └── public/
│       ├── src/js/            # 页面逻辑，按模块拆分
│       ├── src/css/
│       └── *.html
├── docker-compose.yml         # PostgreSQL + 后端编排
├── .env.example               # 环境变量模板
└── README.md
```

---

## 分支说明

本仓库按参赛年份与赛事划分分支，各分支留存对应阶段的完整实现与设计材料：

| 分支 | 内容 |
|------|------|
| `2025-jsjds` | 当前主线。Go 后端 + Web 前端，含容器化与配置管理 |
| `2024-China-Us-Young-Maker-Competition` | 中美青年创客大赛版本。端侧 Python 实现，含情绪识别 Agent、语音合成与表情播放，附设计文档与答辩材料 |
| `2024-Cross-Strait-Information-Innovation-Competition` | 海峡两岸信息创新创业大赛版本 |

端侧感知与反馈能力在 2024 分支中实现，当前主线聚焦云端与前端。

---

## 数据模型

| 表 | 说明 |
|----|------|
| `users` | 账号信息：用户名、邮箱、密码哈希、签名、头像 |
| `emotion_interactions` | 每次互动的快照：语音文本、情绪标签、AI 建议、音视频路径、时间戳、所属周 |
| `community_posts` | 社区帖子：内容、点赞数、作者 |
| `comments` | 帖子评论 |

---

## 已知限制

以下问题是当前版本的已知技术债，已排入后续迭代：

- 情绪记录中的音视频字段保存的是路径字符串，尚未实现文件上传与对象存储，当前要求端与后端共享文件系统。
- 上报接口仅校验 `user_id`，未对设备身份做独立鉴权。
- 数据库结构依赖 GORM `AutoMigrate` 增量同步，尚未引入版本化迁移。
- 前端 `baseURL` 为硬编码，缺少多环境配置。
