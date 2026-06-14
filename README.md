# 自然灾害频发地区情况数据分析及可视化系统

本项目是山东科技大学本科毕业设计《自然灾害频发地区情况数据分析及可视化系统》的配套实现，面向自然灾害历史数据的检索、统计分析、空间可视化和次生灾害关联分析场景。

系统采用前后端分离的 B/S 架构，后端基于 FastAPI 提供 RESTful API，前端基于 Vue3、Naive UI、ECharts 与 Leaflet 构建交互式数据分析页面。系统围绕灾害事件、国家/地区、人员影响、经济损失和灾害关联规则等数据，提供多维度查询、图表分析、地图展示、权限管理与审计日志能力。

## 项目背景

近年来，全球自然灾害呈现高频化、复合化趋势，灾害数据来源分散、结构复杂，传统统计方式难以及时支撑风险监测与应急决策。本系统通过整合自然灾害历史数据，对灾害发生频次、影响人数、伤亡情况、经济损失和不同灾害类型之间的关联关系进行分析，并以图表和地图方式进行展示，为灾害态势研判和次生灾害应对提供辅助参考。

## 核心功能

- 首页概览：展示近年灾害总频次、受影响人数、经济损失和高发灾害类型/国家排行。
- 数据检索：按灾害编号、国家、灾害类型和时间范围查询灾害记录，并结合地图标记展示灾害位置。
- 灾害详情：整合灾害基础信息、地理信息、人员影响和经济损失数据。
- 全球尺度分析：按时间范围统计全球灾害频次、人员影响和直接经济损失，并用柱状图、折线图和饼图展示。
- 国家尺度分析：支持选择国家和统计年限，查看单个国家的灾害频次、影响人数、伤亡人数、经济损失及散点对比分析。
- 态势分析：基于 Leaflet 与 GeoJSON 进行大洲级空间可视化，并提供各国 Top10 排行图。
- 次生灾害分析：基于 Apriori 关联规则挖掘灾害类型之间的关联关系，展示支持度、置信度和提升度，并支持生成智能分析报告。
- 系统管理：提供用户、角色、菜单、API、部门和审计日志管理，支持 JWT 登录认证与 RBAC 权限控制。

## 技术栈

### 后端

- Python 3.11
- FastAPI 0.111
- Uvicorn
- Tortoise-ORM
- Aerich
- MySQL
- Pydantic
- JWT / RBAC
- pandas、mlxtend、scikit-learn

### 前端

- Vue3
- Vite
- Naive UI
- Pinia
- Vue Router
- Axios
- ECharts
- Leaflet
- UnoCSS

## 数据说明

项目中的灾害数据文件位于 `app/data` 目录，主要包括：

- `disasters.csv`：灾害基础信息。
- `countries.csv`：国家/地区信息。
- `human_impact.csv`：人员影响数据。
- `economic_loss.csv`：经济损失数据。
- `associated_types.csv`：灾害关联类型数据。
- `emdat.csv`：用于生成灾害关联规则的原始数据。

后端启动时会根据 `app/data/emdat.csv` 生成关联规则文件：

```text
app/api/v1/association/disaster_association_rules.json
```

## 目录结构

```text
.
├── app                         # 后端应用
│   ├── api                     # API 路由
│   │   └── v1                  # v1 接口模块
│   ├── controllers             # 业务控制层
│   ├── core                    # 中间件、依赖、异常、初始化逻辑
│   ├── data                    # 灾害数据 CSV 文件
│   ├── log                     # 日志模块
│   ├── models                  # Tortoise-ORM 数据模型
│   ├── schemas                 # Pydantic 数据结构
│   ├── settings                # 系统配置
│   └── utils                   # 工具函数
├── migrations                  # Aerich 数据库迁移文件
├── web                         # 前端应用
│   ├── public                  # 公共资源
│   ├── settings                # 前端配置
│   └── src
│       ├── api                 # 前端接口封装
│       ├── components          # 通用组件
│       ├── geojson             # 地图边界数据
│       ├── router              # 路由配置
│       ├── store               # Pinia 状态管理
│       ├── styles              # 全局样式
│       ├── utils               # 前端工具函数
│       └── views               # 页面视图
├── init.sql                    # MySQL 初始化脚本
├── requirements.txt            # Python 依赖
├── pyproject.toml              # Python 项目配置
└── run.py                      # 后端启动入口
```

## 环境要求

- Python 3.11+
- Node.js 18+
- pnpm 或 npm
- MySQL 5.7+ / 8.x

## 后端启动

1. 创建并激活 Python 虚拟环境：

```sh
python -m venv .venv
.\.venv\Scripts\activate
```

Linux / macOS：

```sh
python3 -m venv .venv
source .venv/bin/activate
```

2. 安装依赖：

```sh
pip install -r requirements.txt
```

3. 配置数据库连接：

打开 `app/settings/config.py`，按本地 MySQL 环境修改 `host`、`port`、`user`、`password` 和 `database`。

4. 初始化数据库：

```sh
mysql -u root -p --local-infile=1 mybase < init.sql
```

如果本地 MySQL 禁用了 `local_infile`，需要先开启该配置；同时请根据实际 CSV 存放路径调整 `init.sql` 中的 `LOAD DATA INFILE` 路径。

5. 启动后端服务：

```sh
python run.py
```

后端默认运行在：

```text
http://localhost:9999
```

API 文档地址：

```text
http://localhost:9999/docs
```

## 前端启动

1. 进入前端目录：

```sh
cd web
```

2. 安装依赖：

```sh
pnpm install
```

如果没有安装 pnpm，也可以使用：

```sh
npm install
```

3. 启动开发服务：

```sh
pnpm dev
```

前端启动后根据终端提示访问本地地址。本项目 `web/.env` 中默认端口为 `3100`：

```text
http://localhost:3100
```

## 默认账号

系统初始化时会创建默认管理员账号：

```text
用户名：admin
密码：123456
```

## 主要接口模块

后端接口统一以 `/api/v1` 为前缀，主要模块如下：

- `/base`：登录、用户信息、菜单和用户 API。
- `/disaster`：灾害数据详情、列表、统计和关键字校验。
- `/human_impact`：人员影响、伤亡人数和受影响人数统计。
- `/economic_loss`：经济损失查询与统计。
- `/country`：国家/地区数据管理。
- `/association`：灾害关联规则查询。
- `/user`、`/role`、`/menu`、`/api`、`/dept`、`/auditlog`：系统管理相关接口。

## 论文信息

- 论文题目：自然灾害频发地区情况数据分析及可视化系统
- 英文题目：Data analysis and visualization system for areas with frequent natural disasters
- 作者：姚和艺
- 学校：山东科技大学
- 专业：软件工程
- 完成日期：2025 年 6 月 8 日

## 说明

本项目基于 `vue-fastapi-admin` 后台管理框架进行二次开发，保留了用户、角色、菜单、API 和审计日志等后台基础能力，并在此基础上扩展了自然灾害数据管理、统计分析、空间可视化和次生灾害关联分析等毕业设计业务功能。
